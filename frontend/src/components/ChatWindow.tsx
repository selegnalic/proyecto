import { useEffect, useRef, useState } from "react";
import { useChat } from "../hooks/useChat";
import Message from "./Message";

export default function ChatWindow() {
  const { messages, send, loading, profile, reset } = useChat();
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    send(input);
    setInput("");
  };

  return (
    <>
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4 bg-white">
        {messages.map((m, i) => (
          <Message key={i} msg={m} />
        ))}
        {loading && (
          <div className="flex justify-start mb-3">
            <div className="bg-gray-100 px-4 py-2 rounded-2xl text-sm text-gray-500">
              Escribiendo…
            </div>
          </div>
        )}
      </div>

      {profile && (
        <div className="border-t bg-gray-50 px-4 py-2 text-xs text-gray-600 flex flex-wrap gap-2">
          {profile.skin_type && <span className="bg-white px-2 py-1 rounded">Piel: {profile.skin_type}</span>}
          {profile.age && <span className="bg-white px-2 py-1 rounded">Edad: {profile.age}</span>}
          {profile.goal && <span className="bg-white px-2 py-1 rounded">Objetivo: {profile.goal}</span>}
          {profile.budget && <span className="bg-white px-2 py-1 rounded">Presupuesto: ${profile.budget}</span>}
          <button onClick={reset} className="ml-auto text-rose-500 hover:underline">
            Nueva sesión
          </button>
        </div>
      )}

      <form onSubmit={handleSubmit} className="border-t bg-white p-3 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe tu mensaje…"
          className="flex-1 border rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-rose-300"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-rose-500 text-white px-5 py-2 rounded-full disabled:opacity-50 hover:bg-rose-600"
        >
          Enviar
        </button>
      </form>
    </>
  );
}
