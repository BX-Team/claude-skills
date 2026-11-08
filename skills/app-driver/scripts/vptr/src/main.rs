use std::io::{BufRead, Write};
use std::os::fd::AsFd;
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use wayland_client::{Connection, Dispatch, QueueHandle, globals::{registry_queue_init, GlobalListContents}, protocol::{wl_registry, wl_pointer, wl_seat}};
use wayland_protocols_wlr::virtual_pointer::v1::client::{zwlr_virtual_pointer_manager_v1::ZwlrVirtualPointerManagerV1 as Mgr, zwlr_virtual_pointer_v1::ZwlrVirtualPointerV1 as Ptr};
use wayland_protocols_misc::zwp_virtual_keyboard_v1::client::{zwp_virtual_keyboard_manager_v1::ZwpVirtualKeyboardManagerV1 as KMgr, zwp_virtual_keyboard_v1::ZwpVirtualKeyboardV1 as Kbd};

struct S;
impl Dispatch<wl_registry::WlRegistry, GlobalListContents> for S { fn event(_: &mut S, _: &wl_registry::WlRegistry, _: wl_registry::Event, _: &GlobalListContents, _: &Connection, _: &QueueHandle<S>) {} }
impl Dispatch<Mgr, ()> for S { fn event(_: &mut S, _: &Mgr, _: <Mgr as wayland_client::Proxy>::Event, _: &(), _: &Connection, _: &QueueHandle<S>) {} }
impl Dispatch<Ptr, ()> for S { fn event(_: &mut S, _: &Ptr, _: <Ptr as wayland_client::Proxy>::Event, _: &(), _: &Connection, _: &QueueHandle<S>) {} }
impl Dispatch<KMgr, ()> for S { fn event(_: &mut S, _: &KMgr, _: <KMgr as wayland_client::Proxy>::Event, _: &(), _: &Connection, _: &QueueHandle<S>) {} }
impl Dispatch<Kbd, ()> for S { fn event(_: &mut S, _: &Kbd, _: <Kbd as wayland_client::Proxy>::Event, _: &(), _: &Connection, _: &QueueHandle<S>) {} }
impl Dispatch<wl_seat::WlSeat, ()> for S { fn event(_: &mut S, _: &wl_seat::WlSeat, _: wl_seat::Event, _: &(), _: &Connection, _: &QueueHandle<S>) {} }

fn ms() -> u32 { SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis() as u32 }

fn code(c: char) -> Option<(u32, bool)> {
    let row = |s: &str, base: u32| s.find(c.to_ascii_lowercase()).map(|i| base + i as u32);
    let k = row("qwertyuiop", 16).or_else(|| row("asdfghjkl", 30)).or_else(|| row("zxcvbnm", 44)).or_else(|| row("1234567890", 2))
        .or(match c { ':' => return Some((39, true)), '_' => return Some((12, true)), ' ' => Some(57), '-' => Some(12), '.' => Some(52), '/' => Some(53), _ => None })?;
    Some((k, c.is_ascii_uppercase()))
}

fn main() {
    let size = std::env::var("VPTR_SIZE").unwrap_or_else(|_| "1280x720".into());
    let (w, h) = size.split_once('x').map(|(a, b)| (a.parse::<u32>().unwrap(), b.parse::<u32>().unwrap())).unwrap();
    let conn = Connection::connect_to_env().unwrap();
    let (globals, mut q) = registry_queue_init::<S>(&conn).unwrap();
    let qh = q.handle();
    let mgr: Mgr = globals.bind(&qh, 1..=2, ()).unwrap();
    let ptr = mgr.create_virtual_pointer(None, &qh, ());
    let seat: wl_seat::WlSeat = globals.bind(&qh, 1..=7, ()).unwrap();
    let kmgr: KMgr = globals.bind(&qh, 1..=1, ()).unwrap();
    let kbd = kmgr.create_virtual_keyboard(&seat, &qh, ());
    let keymap = include_bytes!("../keymap.xkb");
    let path = std::env::temp_dir().join(format!("vptr-keymap-{}", std::process::id()));
    let mut f = std::fs::File::create(&path).unwrap();
    f.write_all(keymap).unwrap();
    f.write_all(&[0]).unwrap();
    let f = std::fs::File::open(&path).unwrap();
    kbd.keymap(1, f.as_fd(), keymap.len() as u32 + 1);
    q.roundtrip(&mut S).unwrap();
    let key = |k: u32, down: bool| kbd.key(ms(), k, if down { 1 } else { 0 });
    let tap = |k: u32, shift: bool| {
        if shift { key(42, true); kbd.modifiers(1, 0, 0, 0); }
        key(k, true); conn.flush().unwrap(); std::thread::sleep(Duration::from_millis(25));
        key(k, false);
        if shift { key(42, false); kbd.modifiers(0, 0, 0, 0); }
    };
    for line in std::io::stdin().lock().lines() {
        let line = line.unwrap();
        let p: Vec<&str> = line.splitn(3, ' ').collect();
        match p.as_slice() {
            ["move", x, y] => { ptr.motion_absolute(ms(), (x.parse::<f64>().unwrap() * 16.0) as u32, (y.parse::<f64>().unwrap() * 16.0) as u32, w * 16, h * 16); ptr.frame(); }
            ["click"] | ["rclick"] => {
                let b = if p[0] == "click" { 0x110 } else { 0x111 };
                ptr.button(ms(), b, wl_pointer::ButtonState::Pressed); ptr.frame();
                conn.flush().unwrap(); std::thread::sleep(Duration::from_millis(70));
                ptr.button(ms(), b, wl_pointer::ButtonState::Released); ptr.frame();
            }
            ["down"] => { ptr.button(ms(), 0x110, wl_pointer::ButtonState::Pressed); ptr.frame(); }
            ["up"] => { ptr.button(ms(), 0x110, wl_pointer::ButtonState::Released); ptr.frame(); }
            ["scroll", d] => {
                let d: i32 = d.parse().unwrap();
                ptr.axis_source(wl_pointer::AxisSource::Wheel);
                ptr.axis_discrete(ms(), wl_pointer::Axis::VerticalScroll, 15.0 * d as f64, d);
                ptr.frame();
            }
            ["key", k] => tap(k.parse().unwrap(), false),
            ["type", rest @ ..] => {
                for c in rest.join(" ").chars() {
                    if let Some((k, s)) = code(c) { tap(k, s); conn.flush().unwrap(); std::thread::sleep(Duration::from_millis(40)); }
                }
            }
            _ => {}
        }
        conn.flush().unwrap();
        q.roundtrip(&mut S).unwrap();
        println!("ok");
        std::io::stdout().flush().unwrap();
    }
}
