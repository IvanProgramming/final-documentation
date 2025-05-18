-- configuration -----------------------------------------------------------
local break_command = "\\clearpage"   -- change to \newpage if preferred
local break_block   = pandoc.RawBlock("latex", break_command)
local before_header = true             -- set to false for after-header break

-- filter -----------------------------------------------------------------
function Header(el)
  -- Only affect H1 (level-1) headers
  if el.level == 1 then
    if before_header then
      return { break_block, el }
    else
      return { el, break_block }
    end
  end
  -- leave other header levels untouched
  return nil
end