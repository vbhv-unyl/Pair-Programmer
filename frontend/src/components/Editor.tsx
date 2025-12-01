import React, { useRef, useEffect, useCallback } from "react";
import Editor, { OnChange } from "@monaco-editor/react";

type Props = {
  value: string;
  language?: string;
  onChange: (code: string) => void;
};

export default function CodeEditor({ value, language = "python", onChange }: Props) {
  const editorRef = useRef<any>(null);

  function handleMount(editor: any) {
    editorRef.current = editor;
  }

  // expose programmatic set value when remote update arrives
  useEffect(() => {
    if (!editorRef.current) return;
    const current = editorRef.current.getValue();
    if (value !== current) {
      // Preserve cursor position: try to set without moving cursor too much
      const sel = editorRef.current.getSelection();
      editorRef.current.setValue(value);
      if (sel) editorRef.current.setSelection(sel);
    }
  }, [value]);

  const onEditorChange: OnChange = useCallback(
    (val) => {
      onChange(val || "");
    },
    [onChange]
  );

  return (
    <div className="editor-wrap">
      <Editor
        height="100%"
        defaultLanguage={language}
        language={language}
        value={value}
        onMount={handleMount}
        onChange={onEditorChange}
        options={{
          fontSize: 14,
          minimap: { enabled: false },
        }}
      />
    </div>
  );
}
