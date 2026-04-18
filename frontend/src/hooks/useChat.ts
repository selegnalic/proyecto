import { useCallback, useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const API_URL = `${API_BASE}/api/chat`;
const STORAGE_KEY = "skincare_session_id";

export type Message = {
  role: "user" | "assistant";
  content: string;
};

export type Profile = {
  skin_type: string | null;
  age: number | null;
  goal: string | null;
  budget: number | null;
  ready_to_recommend: boolean;
};

function getSessionId(): string {
  let id = localStorage.getItem(STORAGE_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(STORAGE_KEY, id);
  }
  return id;
}

export function useChat() {
  const [sessionId, setSessionId] = useState<string>(() => getSessionId());
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "¡Hola! Soy tu asesor de skincare. Cuéntame qué tipo de piel tienes y qué te gustaría mejorar.",
    },
  ]);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    document.title = "Asistente de Skincare";
  }, []);

  const send = useCallback(
    async (text: string) => {
      if (!text.trim() || loading) return;
      const userMsg: Message = { role: "user", content: text };
      setMessages((m) => [...m, userMsg]);
      setLoading(true);

      try {
        const res = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId, message: text }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setMessages((m) => [...m, { role: "assistant", content: data.reply }]);
        setProfile(data.state);
      } catch (err) {
        setMessages((m) => [
          ...m,
          { role: "assistant", content: `Error conectando al servidor: ${String(err)}` },
        ]);
      } finally {
        setLoading(false);
      }
    },
    [sessionId, loading]
  );

  const reset = useCallback(() => {
    const id = crypto.randomUUID();
    localStorage.setItem(STORAGE_KEY, id);
    setSessionId(id);
    setMessages([
      {
        role: "assistant",
        content: "Sesión nueva. Cuéntame sobre tu piel.",
      },
    ]);
    setProfile(null);
  }, []);

  return { messages, send, loading, profile, reset, sessionId };
}
