-- Mainframe Latão: the final visual settings override the preserved base.
hl.config({
 misc = { font_family = "IBM Plex Mono" },
 general = { gaps_in = 6, gaps_out = 16, border_size = 2,
   col = { active_border = "rgba(c8743fff)", inactive_border = "rgba(3a3224ff)" } },
 decoration = { rounding = 0, active_opacity = 1.0, inactive_opacity = 1.0,
   blur = { enabled = false }, shadow = { enabled = false } }
})
-- Only the Yazi scratchpad floats; Herdr and everything else tile. Super+V toggles.
hl.window_rule({ match = { class = "^(yazi-special|yazi-toggle)$" }, float = true, size = "1160 740", center = true, opacity = "1.0 override" })
hl.window_rule({ match = { class = "^(herdr-special)$" }, opacity = "1.0 override" })
-- F8 parks the Yazi scratchpad top-left, aligned with the focus gaps (60 + border).
-- The panel's control calls this with `true` on entering/leaving to also re-center.
local runtime = os.getenv("XDG_RUNTIME_DIR") or "/tmp"
local focus_file = runtime .. "/mainframe-" .. (runtime:match("(%d+)$") or "") .. "/focus.json"
function mainframe_place_yazi(center_outside_focus)
  local f = io.open(focus_file, "r")
  if f then f:close() elseif not center_outside_focus then return end
  local m = hl.get_active_monitor()
  for _, w in ipairs(hl.get_windows()) do
    if w.class == "yazi-special" or w.class == "yazi-toggle" then
      local sel = "address:" .. w.address
      if f then hl.dispatch(hl.dsp.window.move({ window = sel, x = m.x + 62, y = m.y + 62 }))
      else hl.dispatch(hl.dsp.window.center({ window = sel })) end
    end
  end
end
hl.on("window.open", function() mainframe_place_yazi() end)
hl.on("workspace.special_active", function() mainframe_place_yazi() end)
hl.bind("SUPER + TAB", hl.dsp.exec_cmd("~/.config/mainframe/control dashboard"))
hl.bind("SUPER + T", hl.dsp.exec_cmd("~/.config/mainframe/control dashboard"))
hl.bind("SUPER + N", hl.dsp.exec_cmd("swaync-client --toggle-panel"))
hl.bind("F8", hl.dsp.exec_cmd("~/.config/mainframe/control focus"))
hl.bind("XF86MonBrightnessUp", hl.dsp.exec_cmd("~/.config/mainframe/control brightness --inc"))
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("~/.config/mainframe/control brightness --dec"))

-- Keep system startup under the existing compositor session.
hl.on("hyprland.start", function()
  hl.exec_cmd("~/.config/mainframe/control start")
end)

-- F7: with a normal/focus pair (hypr_config1/2.lua) it swaps them; otherwise the
-- theme's window focus mode (also on F8).
local swap = os.getenv("HOME") .. "/.config/neobrutal/scripts/focus"
local pair = io.open(os.getenv("HOME") .. "/.config/hypr/hypr_config2.lua", "r")
if pair then pair:close() end
hl.bind("F7", hl.dsp.exec_cmd(pair and ("sh -c '" .. swap .. "'") or "~/.config/mainframe/control focus"))
hl.bind("SUPER + SPACE", hl.dsp.exec_cmd("~/.config/mainframe/control launcher"))
hl.bind("SUPER + O", hl.dsp.exec_cmd("~/.config/mainframe/control clipboard"))
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("~/.config/mainframe/control volume --inc"))
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("~/.config/mainframe/control volume --dec"))
hl.bind("XF86AudioMute", hl.dsp.exec_cmd("~/.config/mainframe/control volume --toggle"))
hl.bind("XF86AudioMicMute", hl.dsp.exec_cmd("~/.config/mainframe/control volume --toggle-mic"))
