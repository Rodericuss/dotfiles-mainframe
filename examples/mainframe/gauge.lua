-- Mainframe Latão · ten-segment phosphor meter
local M = {}

local palette = {
  background = '#0D0C09',
  phosphor = '#9EEA8E',
  brass = '#B8925A',
  copper = '#C8743F',
  patina = '#5BA89B',
}

---Build a bounded ten-segment meter.
---@param value number Percentage, from 0 to 100
---@return string
function M.meter(value)
  local level = math.max(0, math.min(100, value))
  local filled = math.floor(level / 10 + 0.5)
  return string.rep('▮', filled) .. string.rep('▯', 10 - filled)
end

function M.label(value)
  return string.format('VOL %s %d', M.meter(value), value)
end

M.palette = palette
return M
