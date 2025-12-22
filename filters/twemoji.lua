-- Convert Unicode emoji to twemojis commands for LaTeX/PDF output.

if not FORMAT:match("latex") then
  return {}
end

local function is_emoji(cp)
  return (cp >= 0x1F000 and cp <= 0x1FAFF) or (cp >= 0x1F1E6 and cp <= 0x1F1FF)
end

local function cp_hex(cp)
  return string.format("%x", cp)
end

function Str(el)
  local text = el.text
  local inlines = {}
  local buffer = {}

  local function flush()
    if #buffer > 0 then
      table.insert(inlines, pandoc.Str(table.concat(buffer)))
      buffer = {}
    end
  end

  for _, cp in utf8.codes(text) do
    if is_emoji(cp) then
      flush()
      table.insert(inlines, pandoc.RawInline("latex", "\\twemoji{" .. cp_hex(cp) .. "}"))
    else
      table.insert(buffer, utf8.char(cp))
    end
  end

  flush()

  if #inlines == 0 then
    return nil
  end

  return inlines
end
