-- Mainframe Latão: the final visual settings override the preserved base.
hl.config({
 misc = { font_family = "IBM Plex Mono" },
 general = { gaps_in = 6, gaps_out = 16, border_size = 2,
   col = { active_border = "rgba(c8743fff)", inactive_border = "rgba(3a3224ff)" } },
 decoration = { rounding = 0, active_opacity = 1.0, inactive_opacity = 1.0,
   blur = { enabled = false }, shadow = { enabled = false } }
})
-- Compact floating defaults; Super+V still toggles tiling.
hl.window_rule({ match = { class = "^(kitty|neovide)$" }, float = true, size = "1000 650", center = true, opacity = "1.0 override" })
hl.window_rule({ match = { class = "^(firefox)$" }, float = true, size = "1280 820", center = true })
hl.window_rule({ match = { class = "^(herdr-special|yazi-special|yazi-toggle)$" }, float = true, size = "1160 740", center = true, opacity = "1.0 override" })
hl.bind("SUPER + TAB", hl.dsp.exec_cmd("~/.config/mainframe/control dashboard"))
hl.bind("SUPER + T", hl.dsp.exec_cmd("~/.config/mainframe/control dashboard"))
hl.bind("SUPER + N", hl.dsp.exec_cmd("swaync-client --toggle-panel"))
hl.bind("SUPER + ALT + F", hl.dsp.exec_cmd("~/.config/mainframe/control focus"))
hl.bind("XF86MonBrightnessUp", hl.dsp.exec_cmd("~/.config/mainframe/control brightness --inc"))
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("~/.config/mainframe/control brightness --dec"))

-- Keep system startup under the existing compositor session.
hl.on("hyprland.start", function()
  hl.exec_cmd("~/.config/mainframe/control start")
end)

hl.bind("F7", hl.dsp.exec_cmd("~/.config/mainframe/control focus"))
hl.bind("SUPER + SPACE", hl.dsp.exec_cmd("~/.config/mainframe/control launcher"))
hl.bind("SUPER + O", hl.dsp.exec_cmd("~/.config/mainframe/control clipboard"))
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("~/.config/mainframe/control volume --inc"))
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("~/.config/mainframe/control volume --dec"))
hl.bind("XF86AudioMute", hl.dsp.exec_cmd("~/.config/mainframe/control volume --toggle"))
hl.bind("XF86AudioMicMute", hl.dsp.exec_cmd("~/.config/mainframe/control volume --toggle-mic"))
