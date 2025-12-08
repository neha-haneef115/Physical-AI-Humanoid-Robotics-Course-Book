// src/components/useTextSelection.ts
import { useEffect, useState, useCallback } from 'react';

interface UseTextSelectionResult {
  selectedText: string | null;
  hasSelection: boolean;
  clearSelection: () => void;
  getSelectionPosition: () => DOMRect | null;
}

const useTextSelection = (minLength: number = 20): UseTextSelectionResult => {
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const [selectionPosition, setSelectionPosition] = useState<DOMRect | null>(null);

  const handleSelectionChange = useCallback(() => {
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) {
      setSelectedText(null);
      setSelectionPosition(null);
      return;
    }

    const text = selection.toString().trim();
    if (text.length >= minLength) {
      setSelectedText(text);
      
      // Get the position of the selection
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      setSelectionPosition(rect);
    } else {
      setSelectedText(null);
      setSelectionPosition(null);
    }
  }, [minLength]);

  const clearSelection = useCallback(() => {
    const selection = window.getSelection();
    if (selection) {
      selection.removeAllRanges();
    }
    setSelectedText(null);
    setSelectionPosition(null);
  }, []);

  useEffect(() => {
    // Add event listeners for selection changes
    document.addEventListener('selectionchange', handleSelectionChange);
    document.addEventListener('mouseup', handleSelectionChange);
    document.addEventListener('keyup', handleSelectionChange);

    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('keyup', handleSelectionChange);
    };
  }, [handleSelectionChange]);

  return {
    selectedText,
    hasSelection: !!selectedText,
    clearSelection,
    getSelectionPosition: () => selectionPosition,
  };
};

export default useTextSelection;