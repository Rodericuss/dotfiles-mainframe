vim.cmd 'highlight clear'
vim.o.termguicolors = true
vim.o.background = 'dark'
vim.g.colors_name = 'mainframe'
local p = { bg='#0D0C09', panel='#15130E', raised='#1C1912', fg='#E9DFC8', dim='#6E5836', brass='#B8925A', copper='#C8743F', green='#9EEA8E', teal='#5BA89B', blue='#6F93A8', red='#D0553F', yellow='#E0B04E', line='#3A3224', muted='#9A8E73' }
local groups = {
 Normal={fg=p.fg,bg=p.bg}, NormalNC={fg=p.fg,bg=p.bg}, NormalFloat={fg=p.fg,bg=p.panel}, FloatBorder={fg=p.brass,bg=p.panel}, FloatTitle={fg=p.bg,bg=p.brass},
 Cursor={fg=p.bg,bg=p.green}, CursorLine={bg=p.raised}, CursorLineNr={fg=p.fg}, LineNr={fg='#4A4233'}, SignColumn={bg=p.bg}, EndOfBuffer={fg=p.bg}, WinSeparator={fg=p.line},
 Comment={fg=p.dim,italic=true}, Constant={fg=p.teal}, String={fg=p.teal}, Character={fg=p.teal}, Number={fg=p.yellow}, Boolean={fg=p.yellow}, Float={fg=p.yellow},
 Identifier={fg=p.fg}, Function={fg=p.blue}, Statement={fg=p.copper}, Keyword={fg=p.copper}, Operator={fg=p.brass}, PreProc={fg=p.brass}, Type={fg=p.blue}, Special={fg=p.brass}, Delimiter={fg=p.fg},
 Visual={bg=p.raised}, Search={fg=p.bg,bg=p.brass}, IncSearch={fg=p.bg,bg=p.green}, MatchParen={fg=p.bg,bg=p.green}, Error={fg=p.red}, ErrorMsg={fg=p.red}, WarningMsg={fg=p.yellow}, MoreMsg={fg=p.green}, Directory={fg=p.brass},
 Pmenu={fg=p.fg,bg=p.panel}, PmenuSel={fg=p.bg,bg=p.green}, PmenuSbar={bg=p.line}, PmenuThumb={bg=p.brass},
 StatusLine={fg=p.fg,bg=p.panel}, StatusLineNC={fg=p.dim,bg=p.panel}, TabLine={fg=p.dim,bg=p.panel}, TabLineSel={fg=p.fg,bg=p.bg}, TabLineFill={bg=p.panel}, MainframeTabLabel={fg=p.bg,bg=p.brass},
 DiagnosticError={fg=p.red}, DiagnosticWarn={fg=p.yellow}, DiagnosticInfo={fg=p.blue}, DiagnosticHint={fg=p.teal}, DiagnosticVirtualTextError={fg=p.red,bg=p.bg},
 DiffAdd={fg=p.green,bg=p.panel}, DiffChange={fg=p.yellow,bg=p.panel}, DiffDelete={fg=p.red,bg=p.panel}, DiffText={fg=p.bg,bg=p.brass},
 GitSignsAdd={fg=p.green}, GitSignsChange={fg=p.yellow}, GitSignsDelete={fg=p.red},
 NeoTreeNormal={fg=p.fg,bg=p.panel}, NeoTreeNormalNC={fg=p.fg,bg=p.panel}, NeoTreeDirectoryName={fg=p.brass}, NeoTreeDirectoryIcon={fg=p.dim}, NeoTreeFileNameOpened={fg=p.green}, NeoTreeCursorLine={fg=p.bg,bg=p.green}, NeoTreeIndentMarker={fg=p.line}, NeoTreeRootName={fg=p.brass},
 TelescopeNormal={fg=p.fg,bg=p.panel}, TelescopeBorder={fg=p.brass,bg=p.panel}, TelescopeSelection={fg=p.bg,bg=p.green}, TelescopeMatching={fg=p.copper}, TelescopePromptTitle={fg=p.bg,bg=p.brass},
 ['@keyword']={fg=p.copper}, ['@keyword.elixir']={fg=p.copper}, ['@function']={fg=p.blue}, ['@function.call']={fg=p.blue}, ['@function.method.call']={fg=p.blue}, ['@function.builtin']={fg=p.blue}, ['@function.definition']={fg=p.green}, ['@string']={fg=p.teal}, ['@variable']={fg=p.fg}, ['@variable.builtin']={fg=p.brass}, ['@type']={fg=p.blue}, ['@constructor']={fg=p.green}, ['@number']={fg=p.yellow}, ['@comment']={fg=p.dim,italic=true}, ['@markup.heading']={fg=p.green,bold=true}, ['@markup.link']={fg=p.teal,underline=true},
}
for name, value in pairs(groups) do vim.api.nvim_set_hl(0,name,value) end
