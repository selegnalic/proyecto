import ChatWindow from "./components/ChatWindow";

export default function App() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-lg overflow-hidden flex flex-col h-[85vh]">
        <header className="bg-gradient-to-r from-pink-500 to-rose-400 px-6 py-4 text-white">
          <h1 className="text-xl font-semibold">Asistente de Skincare</h1>
          <p className="text-sm opacity-90">Recomendaciones personalizadas según tu piel</p>
        </header>
        <ChatWindow />
      </div>
    </div>
  );
}
