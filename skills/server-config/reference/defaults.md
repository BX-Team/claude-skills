# Verified keys and shipped defaults

Every key the skill's rules touch, with the default upstream ships and upstream's own description, read out of the PaperMC documentation sources and Purpur's config classes at Minecraft 26.2. A key that is not in this file has not been verified: check it against the upstream reference before writing it.

DivineMC changes three inherited defaults, so on DivineMC these are already set:

- `bukkit.yml:settings.query-plugins` → `false`
- `spigot.yml:settings.save-user-cache-on-stop-only` → `true`
- `purpur.yml:settings.use-alternate-keepalive` → `true`

## server.properties

| Key | Default | Upstream description |
| --- | --- | --- |
| `allow-flight` | `false` | Means that users will not be kicked if they fly whilst in Survival mode. This is likely to occur through hacking however there can be false positives. |
| `enforce-secure-profile` | `true` | If set to true, players without a Mojang-signed public key will not be able to connect to the server. |
| `entity-broadcast-range-percentage` | `100` | Controls how close entities need to be before being sent to clients. Higher values means they'll be rendered from farther away, potentially causing more lag. This is expressed the percentage of the default value. For example, setting to 50 will make it half as usual. This mimics the function on the client video settings (not unlike Render Distance, which the client can customize so long as it's under the server's setting). This must be between 10 and 1000 percent. |
| `network-compression-threshold` | `256` | The number of bytes of a packet before it is compressed. Setting to a negative disables compression. |
| `online-mode` | `true` | If set to true, the server checks all connecting players against Minecraft's account database. This requires all connected players to have a valid Minecraft account and makes it impossible for cracked players to connect. |
| `simulation-distance` | `10` | Sets the maximum distance from players that living entities may be located in order to be updated by the server, measured in chunks in each direction of the player (radius, not diameter). If entities are outside this radius, then they will not be ticked by the server nor will they be visible to players. Must be between 3 and 32 inclusive. |
| `view-distance` | `10` | Sets the amount of world data the server sends the client, measured in chunks in each direction of the player (radius, not diameter). It determines the server-side viewing distance (Default: 10, Min: 3, Max: 32). |

## bukkit.yml

| Key | Default | Upstream description |
| --- | --- | --- |
| `chunk-gc.period-in-ticks` | `600` | How long chunks loaded by plugins should last for. Capped by Paper to be 20 ticks (1 second). |
| `settings.query-plugins` | `true` | Whether to send plugins in the GS4 Query protocol response. |
| `spawn-limits.ambient` | `15` | Set the spawn-limits for ambient mobs. This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_spawn_limits_ambient). |
| `spawn-limits.animals` | `10` | Set the spawn-limits for animals. This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_spawn_limits_creature). |
| `spawn-limits.axolotls` | `5` | Set the spawn-limits for axolotls. This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_spawn_limits_axolotls). |
| `spawn-limits.monsters` | `70` | Set the spawn-limits for monsters. This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_spawn_limits_monster). |
| `spawn-limits.water-ambient` | `20` | Set the spawn-limits for water ambient mobs. This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_spawn_limits_water_ambient). |
| `spawn-limits.water-animals` | `5` | Set the spawn-limits for water animals. This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_spawn_limits_water_creature). |
| `spawn-limits.water-underground-creature` | `5` | Set the spawn-limits for water underground creatures. This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_spawn_limits_underground_water_creature). |
| `ticks-per.ambient-spawns` | `1` | Number of ticks between each ambient mob spawn attempt. Set to -1 to use [the Vanilla default](https://minecraft.wiki/w/Mob_spawning#Spawn_cycle). This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_ticks_per_spawn_ambient). |
| `ticks-per.animal-spawns` | `400` | Number of ticks between each passive creature (animal) spawn attempt. Set to -1 to use [the Vanilla default](https://minecraft.wiki/w/Mob_spawning#Spawn_cycle). This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_ticks_per_spawn_creature). |
| `ticks-per.axolotl-spawns` | `1` | Number of ticks between each axolotl spawn attempt. Set to -1 to use [the Vanilla default](https://minecraft.wiki/w/Mob_spawning#Spawn_cycle). This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_ticks_per_spawn_axolotls). |
| `ticks-per.monster-spawns` | `1` | Number of ticks between each hostile monster spawn attempt. Set to -1 to use [the Vanilla default](https://minecraft.wiki/w/Mob_spawning#Spawn_cycle). This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_ticks_per_spawn_monster). |
| `ticks-per.water-ambient-spawns` | `1` | Number of ticks between each ambient water mob spawn attempt. Set to -1 to use [the Vanilla default](https://minecraft.wiki/w/Mob_spawning#Spawn_cycle). This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_ticks_per_spawn_water_ambient). |
| `ticks-per.water-spawns` | `1` | Number of ticks between each water creature spawn attempt. Set to -1 to use [the Vanilla default](https://minecraft.wiki/w/Mob_spawning#Spawn_cycle). This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_ticks_per_spawn_water_creature). |
| `ticks-per.water-underground-creature-spawns` | `1` | Number of ticks between each underground water creatures spawn attempt. Set to -1 to use [the Vanilla default](https://minecraft.wiki/w/Mob_spawning#Spawn_cycle). This can be overridden by the [Paper world config](https://docs.papermc.io/paper/reference/world-configuration#entities_spawning_ticks_per_spawn_underground_water_creature). |

## spigot.yml

| Key | Default | Upstream description |
| --- | --- | --- |
| `settings.bungeecord` | `false` | Whether to enable Bungeecord support, enabling: - Receiving forwarded player-data and source ips. - Support for binding to unix domain sockets. |
| `settings.log-named-deaths` | `true` | Whether to log deaths of entities with custom names to console and latest.log |
| `settings.log-villager-deaths` | `true` | Whether to log villager deaths and witch transformations to console and latest.log |
| `settings.netty-threads` | `4` | Sets number of netty threads. |
| `settings.save-user-cache-on-stop-only` | `false` | If false, the server saves the user-cache on every update. |
| `world-settings.default.arrow-despawn-rate` | `1200` | The number of ticks before an arrow despawns. |
| `world-settings.default.entity-activation-range.animals` | `32` | The entity activation range for animals. |
| `world-settings.default.entity-activation-range.flying-monsters` | `32` | The entity activation range for flying monsters. |
| `world-settings.default.entity-activation-range.ignore-spectators` | `false` | Whether spectators activate entities within range. |
| `world-settings.default.entity-activation-range.misc` | `16` | The entity activation range for miscellaneous entities, including dropped items. Outside of this range, items moving through water streams may appear to visually lag, rubber-band, or move backward. |
| `world-settings.default.entity-activation-range.monsters` | `32` | The entity activation range for monsters. |
| `world-settings.default.entity-activation-range.raiders` | `64` | The entity activation range for raiders. |
| `world-settings.default.entity-activation-range.tick-inactive-villagers` | `true` | Whether to keep ticking villagers that are outside of their activation range. |
| `world-settings.default.entity-activation-range.villagers` | `32` | The entity activation range for villagers. |
| `world-settings.default.entity-activation-range.wake-up-inactive.animals-for` | `100` | How long to wake an inactive animal up for, in ticks. |
| `world-settings.default.entity-activation-range.wake-up-inactive.animals-max-per-tick` | `4` | A limit of how many inactive animals can be woken up on the same tick. |
| `world-settings.default.entity-activation-range.wake-up-inactive.flying-monsters-for` | `100` | How long to wake an inactive flying monster up for, in ticks. |
| `world-settings.default.entity-activation-range.wake-up-inactive.flying-monsters-max-per-tick` | `8` | A limit of how many inactive flying monsters can be woken up on the same tick. |
| `world-settings.default.entity-activation-range.wake-up-inactive.monsters-for` | `100` | How long to wake an inactive monster up for, in ticks. |
| `world-settings.default.entity-activation-range.wake-up-inactive.monsters-max-per-tick` | `8` | A limit of how many inactive monsters can be woken up on the same tick. |
| `world-settings.default.entity-activation-range.wake-up-inactive.villagers-for` | `100` | How long to wake an inactive villager up for, in ticks. |
| `world-settings.default.entity-activation-range.wake-up-inactive.villagers-max-per-tick` | `4` | A limit of how many inactive villagers can be woken up on the same tick. |
| `world-settings.default.entity-activation-range.water` | `16` | The entity activation range for water mobs. |
| `world-settings.default.entity-tracking-range.animals` | `96` | Controls how far in blocks animals are tracked (sent to) the player. This is scaled by the [entity-broadcast-range-percentage](https://docs.papermc.io/paper/reference/server-properties#entity_broadcast_range_percentage). |
| `world-settings.default.entity-tracking-range.misc` | `96` | Controls how far in blocks misc entities are tracked (sent to) the player. This is scaled by the [entity-broadcast-range-percentage](https://docs.papermc.io/paper/reference/server-properties#entity_broadcast_range_percentage). |
| `world-settings.default.entity-tracking-range.monsters` | `96` | Controls how far in blocks monsters are tracked (sent to) the player. This is scaled by the [entity-broadcast-range-percentage](https://docs.papermc.io/paper/reference/server-properties#entity_broadcast_range_percentage). |
| `world-settings.default.entity-tracking-range.other` | `64` | Controls how far in blocks other entities are tracked (sent to) the player. This is scaled by the [entity-broadcast-range-percentage](https://docs.papermc.io/paper/reference/server-properties#entity_broadcast_range_percentage). |
| `world-settings.default.entity-tracking-range.players` | `128` | Controls how far in blocks players are tracked (sent to) the player. This is scaled by the [entity-broadcast-range-percentage](https://docs.papermc.io/paper/reference/server-properties#entity_broadcast_range_percentage). |
| `world-settings.default.hanging-tick-frequency` | `100` | How often to tick hanging entities, in ticks. |
| `world-settings.default.max-tnt-per-tick` | `100` | How many TNT to process per server tick. Set to 0 or less to disable. |
| `world-settings.default.merge-radius.exp` | `-1` | The range, in blocks, that exp orbs will combine at on initial spawn. This behavior is not present in Vanilla and doesn't impact the usual merge range once spawned. Set to 0 or less to disable. |
| `world-settings.default.merge-radius.item` | `0.5` | The range, in blocks, that items will combine within. |
| `world-settings.default.mob-spawn-range` | `8` | The range, in chunks, from the player, that mobs can spawn. |
| `world-settings.default.nerf-spawner-mobs` | `false` | Disable most AI for spawner spawned mobs. |
| `world-settings.default.ticks-per.hopper-check` | `1` | The ticks between checks to pull items. |
| `world-settings.default.ticks-per.hopper-transfer` | `8` | The ticks between hopper item movements. |

## config/paper-global.yml

| Key | Default | Upstream description |
| --- | --- | --- |
| `item-validation.book-size.page-max` | `2560` | The max number of bytes a single page in a book can contribute to the allowed byte total for a book, or "disabled" to disable non-vanilla restrictions on the book size. |
| `item-validation.book-size.total-multiplier` | `0.98` | Each page has this multiple of bytes from the last page as its contribution to the allowed byte total for a book (with the first page being having a multiplier of 1.0) |
| `item-validation.book.author` | `8192` | The maximum length of a book's author in characters |
| `item-validation.book.page` | `16384` | The maximum length of a book's page in characters |
| `item-validation.book.title` | `8192` | The maximum length of a book's title in characters |
| `item-validation.display-name` | `8192` | The maximum length of an item's display name in characters |
| `item-validation.lore-line` | `8192` | The maximum length of a lore line in characters |
| `item-validation.resolve-selectors-in-books` | `false` | Whether to resolve selectors in books. With this enabled, players given creative mode will be able to crash the server in yet another way |
| `misc.max-joins-per-tick` | `5` | Sets the maximum amount of players that may join the server in a single tick. If more players join, they will be postponed until later ticks to join but not kicked. This is not related to connection throttling found in bukkit.yml |
| `packet-limiter.all-packets.action` | `KICK` | The action to take once the limit has been violated. Possible values are DROP which will ignore packets over the limit, and KICK which will kick players for exceeding the limit |
| `packet-limiter.all-packets.interval` | `7` | The interval, in seconds, for which max-packet-rate should apply |
| `packet-limiter.all-packets.max-packet-rate` | `500` | The number of packets allowed per player within the interval |
| `packet-limiter.overrides.minecraft:command_suggestion.action` | _unset_ | The action to take once the limit has been violated. Possible values are DROP which will ignore packets over the limit, and KICK which will kick players for exceeding the limit |
| `packet-limiter.overrides.minecraft:command_suggestion.interval` | _unset_ | The interval, in seconds, for which max-packet-rate should apply |
| `packet-limiter.overrides.minecraft:command_suggestion.max-packet-rate` | _unset_ | The number of packets allowed per player within the interval |
| `packet-limiter.overrides.minecraft:container_button_click.action` | _unset_ | The action to take once the limit has been violated. Possible values are DROP which will ignore packets over the limit, and KICK which will kick players for exceeding the limit |
| `packet-limiter.overrides.minecraft:container_button_click.interval` | _unset_ | The interval, in seconds, for which max-packet-rate should apply |
| `packet-limiter.overrides.minecraft:container_button_click.max-packet-rate` | _unset_ | The number of packets allowed per player within the interval |
| `packet-limiter.overrides.minecraft:container_click.action` | _unset_ | The action to take once the limit has been violated. Possible values are DROP which will ignore packets over the limit, and KICK which will kick players for exceeding the limit |
| `packet-limiter.overrides.minecraft:container_click.interval` | _unset_ | The interval, in seconds, for which max-packet-rate should apply |
| `packet-limiter.overrides.minecraft:container_click.max-packet-rate` | _unset_ | The number of packets allowed per player within the interval |
| `packet-limiter.overrides.minecraft:custom_payload.action` | _unset_ | The action to take once the limit has been violated. Possible values are DROP which will ignore packets over the limit, and KICK which will kick players for exceeding the limit |
| `packet-limiter.overrides.minecraft:custom_payload.interval` | _unset_ | The interval, in seconds, for which max-packet-rate should apply |
| `packet-limiter.overrides.minecraft:custom_payload.max-packet-rate` | _unset_ | The number of packets allowed per player within the interval |
| `packet-limiter.overrides.minecraft:interact.action` | _unset_ | The action to take once the limit has been violated. Possible values are DROP which will ignore packets over the limit, and KICK which will kick players for exceeding the limit |
| `packet-limiter.overrides.minecraft:interact.interval` | _unset_ | The interval, in seconds, for which max-packet-rate should apply |
| `packet-limiter.overrides.minecraft:interact.max-packet-rate` | _unset_ | The number of packets allowed per player within the interval |
| `packet-limiter.overrides.minecraft:place_recipe.action` | _unset_ | The action to take once the limit has been violated. Possible values are DROP which will ignore packets over the limit, and KICK which will kick players for exceeding the limit |
| `packet-limiter.overrides.minecraft:place_recipe.interval` | _unset_ | The interval, in seconds, for which max-packet-rate should apply |
| `packet-limiter.overrides.minecraft:place_recipe.max-packet-rate` | _unset_ | The number of packets allowed per player within the interval |
| `packet-limiter.overrides.minecraft:player_action.action` | _unset_ | The action to take once the limit has been violated. Possible values are DROP which will ignore packets over the limit, and KICK which will kick players for exceeding the limit |
| `packet-limiter.overrides.minecraft:player_action.interval` | _unset_ | The interval, in seconds, for which max-packet-rate should apply |
| `packet-limiter.overrides.minecraft:player_action.max-packet-rate` | _unset_ | The number of packets allowed per player within the interval |
| `packet-limiter.overrides.minecraft:set_creative_mode_slot.action` | _unset_ | The action to take once the limit has been violated. Possible values are DROP which will ignore packets over the limit, and KICK which will kick players for exceeding the limit |
| `packet-limiter.overrides.minecraft:set_creative_mode_slot.interval` | _unset_ | The interval, in seconds, for which max-packet-rate should apply |
| `packet-limiter.overrides.minecraft:set_creative_mode_slot.max-packet-rate` | _unset_ | The number of packets allowed per player within the interval |
| `packet-limiter.overrides.minecraft:use_item_on.action` | _unset_ | The action to take once the limit has been violated. Possible values are DROP which will ignore packets over the limit, and KICK which will kick players for exceeding the limit |
| `packet-limiter.overrides.minecraft:use_item_on.interval` | _unset_ | The interval, in seconds, for which max-packet-rate should apply |
| `packet-limiter.overrides.minecraft:use_item_on.max-packet-rate` | _unset_ | The number of packets allowed per player within the interval |
| `proxies.bungee-cord.online-mode` | `true` | Instructs the server how to handle player UUIDs and data when behind BungeeCord. Always set to match your proxy's online-mode setting |
| `proxies.velocity.enabled` | `false` | Whether the server should accept Velocity Modern Forwarding |
| `proxies.velocity.online-mode` | `true` | Instructs the server how to handle player UUIDs and data when behind Velocity. Always set to match your proxy's online-mode setting |
| `unsupported-settings.allow-headless-pistons` | `false` | Whether the server should allow the creation of headless pistons. These are often used to break permanent blocks |
| `unsupported-settings.allow-permanent-block-break-exploits` | `false` | Whether unbreakable blocks can be broken with Vanilla exploits. This includes bedrock, end portal frames, end portal blocks, and more |
| `unsupported-settings.allow-piston-duplication` | `false` | Whether to allow duplication of TNT, carpets, and rails. This does not control sand duplication |

## config/paper-world-defaults.yml

| Key | Default | Upstream description |
| --- | --- | --- |
| `anticheat.anti-xray.enabled` | `false` | Controls the on/off state for the Anti-Xray system |
| `chunks.entity-per-chunk-save-limit.area_effect_cloud` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.arrow` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.breeze_wind_charge` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.dragon_fireball` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.egg` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.ender_pearl` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.experience_bottle` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.experience_orb` | `-1` | Limits the number of experience_orb's that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. |
| `chunks.entity-per-chunk-save-limit.eye_of_ender` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.fireball` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.firework_rocket` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.lingering_potion` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.llama_spit` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.shulker_bullet` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.small_fireball` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.snowball` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.spectral_arrow` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.splash_potion` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.trident` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.wind_charge` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.entity-per-chunk-save-limit.wither_skull` | _unset_ | Limits the number of any type of entity that will be saved/loaded per chunk. A value of -1 disables the limit for a specific entity. **Any entity may be added to the list**, beyond the enumerated defaults |
| `chunks.max-auto-save-chunks-per-tick` | `24` | The maximum number of chunks the auto-save system will save in a single tick |
| `chunks.prevent-moving-into-unloaded-chunks` | `false` | Sets whether the server will prevent players from moving into unloaded chunks or not |
| `collisions.fix-climbing-bypassing-cramming-rule` | `false` | Sets whether climbing should bypass the entity cramming limit(maxEntityCramming game rule). If set to true, climbing entities will also be counted towards the entity cramming limit so that they can take suffocation damage |
| `collisions.max-entity-collisions` | `8` | Instructs the server to stop processing collisions after this value is reached |
| `entities.armor-stands.do-collision-entity-lookups` | `true` | Instructs armor stand entities to do entity collision checks |
| `entities.armor-stands.tick` | `true` | Disable to prevent armor stands from ticking. Can improve performance with many armor stands |
| `entities.behavior.disable-chest-cat-detection` | `false` | Allows you to open chests even if they have a cat sitting on top of them |
| `entities.behavior.parrots-are-unaffected-by-player-movement` | `false` | Makes parrots "sticky" so they do not fall off a player's shoulder when they move. Use crouch to shake them off |
| `entities.behavior.zombies-target-turtle-eggs` | `true` | Sets whether zombies and zombified piglins should target turtle eggs. Setting this to false may help with performance, as they won't search for nearby eggs |
| `entities.markers.tick` | `true` | Disable to prevent markers from ticking. This may affect how they behave as passengers of other entities |
| `entities.spawning.alt-item-despawn-rate.enabled` | `false` | Determines if items will have different despawn rates |
| `entities.spawning.alt-item-despawn-rate.items.acacia_leaves` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.andesite` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.bamboo` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.birch_leaves` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.cactus` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.cherry_leaves` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.cobblestone` | `300` | Sets a custom despawn rate for cobblestone of 300 ticks |
| `entities.spawning.alt-item-despawn-rate.items.dark_oak_leaves` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.diorite` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.dirt` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.granite` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.gravel` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.jungle_leaves` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.kelp` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.mangrove_leaves` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.melon_slice` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.netherrack` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.oak_leaves` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.pumpkin` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.red_sand` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.sand` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.scaffolding` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.short_grass` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.spruce_leaves` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.sugar_cane` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.twisting_vines` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.alt-item-despawn-rate.items.weeping_vines` | _unset_ | Determines how long each respective item despawns in ticks. The item ids are the same as those used in the /give command. They can be viewed by enabling advanced item tooltips in-game by pressing **F3 + H**; the item id will appear at the bottom of the tooltip that appears when you hover over an item |
| `entities.spawning.creative-arrow-despawn-rate` | _unset_ | The rate, in ticks, at which arrows shot from players in creative mode are despawned |
| `entities.spawning.despawn-ranges.ambient.hard` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be forcibly despawned. |
| `entities.spawning.despawn-ranges.ambient.soft` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be randomly selected to be despawned. |
| `entities.spawning.despawn-ranges.axolotls.hard` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be forcibly despawned. |
| `entities.spawning.despawn-ranges.axolotls.soft` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be randomly selected to be despawned. |
| `entities.spawning.despawn-ranges.creature.hard` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be forcibly despawned. |
| `entities.spawning.despawn-ranges.creature.soft` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be randomly selected to be despawned. |
| `entities.spawning.despawn-ranges.misc.hard` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be forcibly despawned. |
| `entities.spawning.despawn-ranges.misc.soft` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be randomly selected to be despawned. |
| `entities.spawning.despawn-ranges.monster.hard` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be forcibly despawned. |
| `entities.spawning.despawn-ranges.monster.soft` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be randomly selected to be despawned. |
| `entities.spawning.despawn-ranges.underground_water_creature.hard` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be forcibly despawned. |
| `entities.spawning.despawn-ranges.underground_water_creature.soft` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be randomly selected to be despawned. |
| `entities.spawning.despawn-ranges.water_ambient.hard` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be forcibly despawned. |
| `entities.spawning.despawn-ranges.water_ambient.soft` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be randomly selected to be despawned. |
| `entities.spawning.despawn-ranges.water_creature.hard` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be forcibly despawned. |
| `entities.spawning.despawn-ranges.water_creature.soft` | _unset_ | The horizontal and vertical number of blocks away from a player in which each monster type (set individually) will be randomly selected to be despawned. |
| `entities.spawning.non-player-arrow-despawn-rate` | _unset_ | The rate, in ticks, at which arrows shot from non-player entities are despawned. The default value instructs the server to use the same default arrow despawn rate from spigot.yml that is used for all arrows |
| `environment.max-block-ticks` | `65536` | The maximum number of block ticks that can be processed in a single tick. This is a safety measure to prevent the server from hanging when there is a large amount of block updates. |
| `environment.max-fluid-ticks` | `65536` | The maximum number of fluid ticks that can be processed in a single tick. This is a safety measure to prevent the server from hanging when there is a large number of fluid updates. |
| `environment.nether-ceiling-void-damage-height` | _unset_ | Sets the level above which players in the nether will take void damage. This is a Vanilla-friendly way to restrict players from using the nether ceiling as a buildable area. Setting to disabled disables this feature |
| `environment.optimize-explosions` | `false` | Instructs the server to cache entity lookups during an explosion, rather than recalculating throughout the process. This speeds up explosions significantly |
| `environment.treasure-maps.enabled` | `true` | If villagers should trade treasure maps and treasure maps from chests should lead to a feature |
| `environment.treasure-maps.find-already-discovered.loot-tables` | _unset_ | Overrides the loot table-configured check for undiscovered structures. default allows loot tables to individually determine if the map should allow discovered locations in its search. All Vanilla loot tables default to skipping discovered locations so changing this to false would override that behavior and force them to search discovered locations |
| `environment.treasure-maps.find-already-discovered.villager-trade` | `false` | Instructs the server to target the first treasure location found for maps obtained via trading with villagers |
| `fixes.fix-items-merging-through-walls` | `false` | Whether items should be prevented from merging through walls. Enabling this will incur a performance degradation. This is only necessary when merge-radius.item (spigot.yml) is large enough to merge items through walls |
| `hopper.disable-move-event` | `false` | Completely disables the InventoryMoveItemEvent for hoppers. Dramatically improves hopper performance but will break protection plugins and any others that depend on this event |
| `hopper.ignore-occluding-blocks` | `false` | Determines if hoppers will ignore containers inside occluding blocks, like a hopper minecart inside a sand block. Enabling this will improve performance for hoppers checking where to insert items |
| `maps.item-frame-cursor-limit` | `128` | The number of cursors (markers) allowed per map. A large number of cursors may be used to lag clients |
| `maps.item-frame-cursor-update-interval` | `10` | The interval in ticks at which cursors on maps in item frames are updated. Setting this to a number less than 1 will disable updates altogether |
| `misc.disable-relative-projectile-velocity` | `false` | Instructs the server to ignore shooter velocity when calculating the velocity of a fired arrow |
| `misc.redstone-implementation` | `VANILLA` | Specifies the redstone implementation that the server uses. Alternative implementations can greatly reduce the lag caused by redstone dust by optimizing power calculations and reducing the number of block and shape updates emitted. The following implementations are available: - **VANILLA**: The Vanilla redstone implementation. - **EIGENCRAFT**: The Eigencraft redstone implementation by theosib. - **ALTERNATE_CURRENT**: The Alternate Current redstone implementation by Space Walker. **Note:** Both the Eigencraft and Alternate Current implementations change the behavior of redstone dust. You can read about how behavior is changed in each implementation's respective documentation: - Eigencraft: No official documentation available. However, [theosib's comments](https://mojira.dev/MC-81098#comment-id-71035) on the Mojira bug tracker give an overview of the Eigencraft implementation. - [Alternate Current](https://github.com/SpaceWalkerRS/alternate-current/blob/main/README.md) |
| `misc.update-pathfinding-on-block-update` | `true` | Controls whether the pathfinding of mobs is updated when a block is updated in the world. Disabling this option can improve the server performance significantly, while there is almost no noticeable effect on the game mechanics. This is recommended when there are lots of entities loaded, and you have automated farms or redstone clocks |
| `tick-rates.behavior.villager.acquirepoi` | _unset_ | Sets the behavior tick rate of an entity. -1 uses Vanilla. See timings for the names. Might change between updates! |
| `tick-rates.behavior.villager.validatenearbypoi` | `-1` | Sets the tick rate of the validatenearbypoi behavior. of Villager entities |
| `tick-rates.dry-farmland` | `1` | Controls how frequently dry farmland blocks are ticked. Higher values slow down the rate at which farmland checks for moisture updates. Default (1) uses Vanilla behavior, -1 disables dry farmland random ticks. |
| `tick-rates.grass-spread` | `1` | Sets the delay, in ticks, at which the server attempts to spread grass. Higher values will result in a slower spread |
| `tick-rates.mob-spawner` | `1` | How often mob spawners should tick to calculate available spawn areas and spawn new entities into the world. A value of -1 will disable all spawners |
| `tick-rates.sensor.villager.nearestbedsensor` | _unset_ | Sets the sensor tick rate of an entity. -1 uses Vanilla. See timings for the names. Might change between updates! |
| `tick-rates.sensor.villager.nearestlivingentitysensor` | _unset_ | Sets the sensor tick rate of an entity. -1 uses Vanilla. See timings for the names. Might change between updates! |
| `tick-rates.sensor.villager.playersensor` | _unset_ | Sets the sensor tick rate of an entity. -1 uses Vanilla. See timings for the names. Might change between updates! |
| `tick-rates.sensor.villager.secondarypoisensor` | `40` | Sets the tick rate of the secondarypoisensor sensor of Villager entities |
| `tick-rates.sensor.villager.villagerbabiessensor` | _unset_ | Sets the sensor tick rate of an entity. -1 uses Vanilla. See timings for the names. Might change between updates! |
| `tick-rates.wet-farmland` | `1` | Controls how frequently wet farmland blocks are ticked. Higher values slow down the rate at which farmland checks for moisture updates. Default (1) uses Vanilla behavior, -1 disables wet farmland random ticks. |

## purpur.yml

| Key | Default | Upstream description |
| --- | --- | --- |
| `settings.lagging-threshold` | `19` | The TPS below which Purpur considers the server to be lagging. |
| `settings.logger.suppress-ignored-advancement-warnings` | `false` | Hides warnings about advancements the server ignored. |
| `settings.logger.suppress-init-legacy-material-errors` | `false` | Hides the legacy material warnings plugins produce on load. |
| `settings.logger.suppress-library-loader` | `false` | Hides the library loader chatter on startup. |
| `settings.logger.suppress-setblock-in-far-chunk-errors` | `false` | Hides the setblock-in-a-far-chunk errors plugins trigger. |
| `settings.logger.suppress-unrecognized-recipe-errors` | `false` | Hides errors about recipes the server does not recognise. |
| `settings.use-alternate-keepalive` | `false` | Sends a keepalive packet every second and only kicks after 30 seconds with no answer, instead of kicking on one dropped packet. |
| `world-settings.default.blocks.observer.disable-clock` | `false` | Stops two observers facing each other from producing an endless signal. |
| `world-settings.default.gameplay-mechanics.armorstand.can-move-in-water` | `true` | Whether armour stands are pushed by water. |
| `world-settings.default.gameplay-mechanics.armorstand.can-move-in-water-over-fence` | `true` | Whether armour stands are pushed by water over a fence. |
| `world-settings.default.gameplay-mechanics.armorstand.can-movement-tick` | `true` | Whether armour stands are allowed to move at all. |
| `world-settings.default.gameplay-mechanics.entities-can-use-portals` | `true` | Whether entities other than players may travel through portals. |
| `world-settings.default.gameplay-mechanics.player.teleport-if-outside-border` | `false` | Teleports a player who ends up outside the world border back to spawn. |
| `world-settings.default.mobs.dolphin.disable-treasure-searching` | `false` | Stops dolphins from running the structure search they use to lead players to treasure. |
| `world-settings.default.mobs.squid.immune-to-EAR` | `true` | Whether squid ignore the entity activation range from spigot.yml. |
| `world-settings.default.mobs.villager.lobotomize.enabled` | `false` | A villager that cannot path to its destination loses its AI and only restocks its trades. |
| `world-settings.default.mobs.villager.search-radius.acquire-poi` | `AcquirePoi.SCAN_RANGE` | Radius in blocks a villager searches for a job site block. |
| `world-settings.default.mobs.villager.search-radius.nearest-bed-sensor` | `AcquirePoi.SCAN_RANGE` | Radius in blocks a villager searches for a bed. |
| `world-settings.default.mobs.zombie.aggressive-towards-villager-when-lagging` | `true` | Whether zombies keep targeting villagers while the server is below the lagging threshold. |

## divinemc.yml

| Key | Default | Upstream description |
| --- | --- | --- |
| `async.chunk-sending.enable` | `false` | Offloads chunk packet serialization to a thread pool, which can significantly reduce main thread load when many players are loading chunks. A consistent snapshot of the chunk is taken on its owning thread, so packets are always internally consistent and packet order is preserved per player. |
| `async.chunk-sending.max-threads` | `1` | — |
| `async.parallel-sensors.enable` | `false` | Runs the read-only part of brain AI (sensors: nearest-entity scans, line-of-sight raycasts) on a worker thread pool right before the entity ticking phase, instead of on the main thread during each mob's tick. Sensors are a stable top entry in profiler output on servers with many villagers/piglins, and they only read world state, which makes them safe to batch. |
| `async.parallel-world-ticking.enable` | `false` | Enables Parallel World Ticking, which executes each world's tick in a separate thread while ensuring that all worlds complete their tick before the next cycle begins. Read more info about this feature at https://bxteam.org/docs/divinemc/features/parallel-world-ticking |
| `async.parallel-world-ticking.thread-count` | `4` | — |
| `async.pathfinding.max-threads` | `1` | — |
| `async.regionized-chunk-ticking.enable` | `false` | Enables regionized chunk ticking, similar to like Folia works. Read more info about this feature at https://bxteam.org/docs/divinemc/features/regionized-chunk-ticking |
| `async.regionized-chunk-ticking.executor-thread-count` | `4` | The amount of threads to allocate to regionized chunk ticking. |
| `misc.lag-compensation.enabled` | `true` | Improves the player experience when TPS is low |
| `misc.old-features.copper-bulb-1gt` | `false` | Whether to delay the copper lamp by 1 tick when the redstone signal changes. |
| `misc.old-features.crafter-1gt` | `false` | Whether to reduce the frequency of the crafter outputting items to 1 tick. |
| `misc.secure-seed.enable` | `false` | This feature is based on Secure Seed mod by Earthcomputer. Terrain and biome generation remains the same, but all the ores and structures are generated with 1024-bit seed, instead of the usual 64-bit seed. This seed is almost impossible to crack, and there are no weird links between structures. |
| `network.general.disable-disconnect-spam` | `false` | Prevents players being disconnected by 'disconnect.spam' when sending too many chat packets |
| `network.no-chat-reports.enabled` | `false` | Enables or disables the No Chat Reports feature |
| `network.raytrace-entity-culling.enabled` | `false` | Enables Raytrace Entity Culling, a server-side port of tr7zw's EntityCulling mod. Entities that a player provably cannot see (fully hidden behind opaque blocks) are removed from that player's entity tracker. This reduces network bandwidth, improves client FPS and blinds entity-ESP cheats (e.g. freecam/x-ray style hacks cannot see mobs, players or items through walls anymore). Visibility is checked asynchronously via raytracing; when a hidden entity comes into view it is re-tracked within one check interval plus one tracker tick. Players with very high ping may notice entities appearing slightly late when peeking around corners. |
| `performance.chunks.chunk-data-cache-limit` | `32678` | — |
| `performance.chunks.chunk-data-cache-soft-limit` | `8192` | — |
| `performance.dab.activation-distance-mod` | `8` | Modifies an entity's tick frequency. The exact calculation to obtain the tick frequency for an entity is: freq = (distanceToPlayer^2) / (2^value), where value is this configuration setting. Large servers may want to reduce the value to 7, but this value should never be reduced below 6. If you want further away entities to tick more often, set the value to 9 |
| `performance.dab.enabled` | `false` | Enables DAB feature |
| `performance.dab.start-distance` | `12` | This value determines how far away an entity has to be |
| `performance.optimizations.clump-orbs` | `false` | Clumps experience orbs together to reduce entity count |
| `performance.optimizations.enable-suffocation-optimization` | `true` | Optimizes the suffocation check by selectively skipping the check in a way that still appears vanilla. This option should be left enabled on most servers, but is provided as a configuration option if the vanilla deviation is undesirable. |
| `performance.optimizations.equipment-tracking` | `false` | When enabled, skips repeated checks whether the equipment of an entity changed. |
| `performance.optimizations.hopper-throttle-when-full.enabled` | `false` | When enabled, hoppers will throttle if target container is full. |
| `performance.optimizations.hopper-throttle-when-full.skip-ticks` | `0` | The amount of ticks to skip when the hopper is throttled. |
| `performance.optimizations.optimized-dragon-respawn` | `false` | When enabled, improving performance and reducing lag during the dragon’s resurrection event. |
| `performance.optimizations.sleeping-block-entity` | `false` | When enabled, block entities will enter a sleep state when they are inactive. |
| `performance.optimizations.use-compact-bit-storage` | `false` | Fixes memory waste caused by sending empty chunks as if they contain blocks. Can significantly reduce memory usage. |
| `region-settings.thread-count` | `4` | The number of threads to use for IO operations. |
| `world-settings.default.unsupported-features.allow-tripwire-dupe` | `false` | Bring back MC-59471, MC-129055 on 1.21.2+, which fixed in 1.21.2 snapshots 24w33a and 24w36a |
