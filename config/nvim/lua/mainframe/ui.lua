local M={}
function M.setup()
 vim.o.guifont='IBM Plex Mono:h11'
 vim.o.showtabline=2
 vim.o.fillchars='eob: ,vert:│'
 vim.o.guicursor='n-v-c:block,i-ci-ve:ver25,r-cr:hor20,o:hor50,a:blinkon0'
 vim.o.pumblend=0
 vim.o.winblend=0
 _G.MainframeBufferClick=function(n) if vim.api.nvim_buf_is_valid(n) then vim.api.nvim_set_current_buf(n) end end
 _G.MainframeTabline=function()
   local s='%#MainframeTabLabel# BUF '
   for _,b in ipairs(vim.api.nvim_list_bufs()) do
     if vim.bo[b].buflisted then
       local name=vim.fn.fnamemodify(vim.api.nvim_buf_get_name(b),':t');if name=='' then name='[novo]' end
       name=name:gsub('%%','%%%%')
       s=s..(b==vim.api.nvim_get_current_buf() and '%#TabLineSel#' or '%#TabLine#')..'%'..b..'@v:lua.MainframeBufferClick@ '..name..(vim.bo[b].modified and ' ● ' or '  ')..'%T'
     end
   end
   return s..'%#TabLineFill#%='
 end
 vim.o.tabline='%!v:lua.MainframeTabline()'
 local saved=nil
 vim.api.nvim_create_user_command('MainframeFocus',function()
   if saved then
     for k,v in pairs(saved) do vim.o[k]=v end;saved=nil
   else
     saved={number=vim.o.number,relativenumber=vim.o.relativenumber,laststatus=vim.o.laststatus,showtabline=vim.o.showtabline,signcolumn=vim.o.signcolumn}
     vim.o.number=false;vim.o.relativenumber=false;vim.o.laststatus=0;vim.o.showtabline=0;vim.o.signcolumn='no'
   end
 end,{})
 vim.keymap.set('n','<leader>uz','<cmd>MainframeFocus<cr>',{desc='Mainframe: foco de leitura'})
end
return M
