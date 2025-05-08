-- figure.lua : оборачивает все картинки в окружение figure
function Image(el)
    -- переносим width/height из атрибутов в \includegraphics
    local opts = ""
    if el.attributes.width then
      opts = opts .. "width=" .. el.attributes.width .. ","
    end
    if el.attributes.height then
      opts = opts .. "height=" .. el.attributes.height .. ","
    end
    if opts ~= "" then
      opts = "[" .. opts:sub(1, -2) .. "]"  -- убираем последний «,»
    end
  
    -- собираем LaTeX код
    local latex = string.format([[
    \includegraphics[width=0.75\linewidth]{%s}
]],
      el.src)
  
    return pandoc.RawInline('latex', latex)
  end
  