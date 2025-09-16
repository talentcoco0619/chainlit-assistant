import { useState } from "react";

export default function SimpleToggleContent() {
  const [isContentVisible, setIsContentVisible] = useState(false);

  const toggleContent = () => {
    setIsContentVisible(!isContentVisible);
  };

  return (
    <div>
      <button onClick={toggleContent}>Toggle Content</button>
      {isContentVisible && (
        <div style={{ marginTop: "10px", marginBottom: "10px" }}>
          <p>This is the content displayed below the button.</p>
        </div>
      )}
    </div>
  );
}

// Lightweight titled section that can be toggled open/closed
export function ToggleSection({ title = "Section", defaultOpen = false, children }) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 6, marginTop: 8 }}>
      <button
        onClick={() => setOpen(!open)}
        style={{
          width: "100%",
          textAlign: "left",
          padding: "8px 10px",
          background: "#f9fafb",
          border: "none",
          borderBottom: open ? "1px solid #e5e7eb" : "none",
          cursor: "pointer",
          fontWeight: 600
        }}
      >
        {title} {open ? "▲" : "▼"}
      </button>
      {open && <div style={{ padding: 10 }}>{children}</div>}
    </div>
  );
}

// Single-open accordion built from ToggleSection-like rows
export function Accordion({ items = [], defaultOpenIndex = -1 }) {
  const [openIndex, setOpenIndex] = useState(defaultOpenIndex);

  const onToggle = (idx) => {
    setOpenIndex((curr) => (curr === idx ? -1 : idx));
  };

  return (
    <div>
      {items.map((item, idx) => {
        const isOpen = idx === openIndex;
        return (
          <div
            key={idx}
            style={{
              border: "1px solid #e5e7eb",
              borderRadius: 6,
              marginTop: 8,
              overflow: "hidden"
            }}
          >
            <button
              onClick={() => onToggle(idx)}
              style={{
                width: "100%",
                textAlign: "left",
                padding: "8px 10px",
                background: "#f9fafb",
                border: "none",
                borderBottom: isOpen ? "1px solid #e5e7eb" : "none",
                cursor: "pointer",
                fontWeight: 600
              }}
            >
              {item.title} {isOpen ? "▲" : "▼"}
            </button>
            {isOpen && <div style={{ padding: 10 }}>{item.content}</div>}
          </div>
        );
      })}
    </div>
  );
}

// Minimal controlled/uncontrolled select
export function SimpleSelect({
  label = "Choose an option",
  options = [],
  value,
  onChange
}) {
  const [internal, setInternal] = useState(value ?? "");

  const handleChange = (e) => {
    const v = e.target.value;
    if (onChange) onChange(v);
    setInternal(v);
  };

  const current = value !== undefined ? value : internal;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6, marginTop: 10 }}>
      <label style={{ fontSize: 12, color: "#374151" }}>{label}</label>
      <select
        value={current}
        onChange={handleChange}
        style={{
          padding: "6px 8px",
          border: "1px solid #d1d5db",
          borderRadius: 6,
          background: "white"
        }}
      >
        <option value="" disabled>
          -- select --
        </option>
        {options.map((opt, idx) => {
          const val = typeof opt === "string" ? opt : opt.value;
          const text = typeof opt === "string" ? opt : opt.label ?? opt.value;
          return (
            <option key={idx} value={val}>
              {text}
            </option>
          );
        })}
      </select>
    </div>
  );
}