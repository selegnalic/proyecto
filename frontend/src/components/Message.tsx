import type { Message as MessageType } from "../hooks/useChat";

export default function Message({ msg }: { msg: MessageType }) {
  const isUser = msg.role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
      <div
        className={`max-w-[75%] px-4 py-2 rounded-2xl whitespace-pre-wrap text-sm leading-relaxed ${
          isUser
            ? "bg-rose-500 text-white rounded-br-sm"
            : "bg-gray-100 text-gray-900 rounded-bl-sm"
        }`}
      >
        {msg.content}
      </div>
    </div>
  );
}
