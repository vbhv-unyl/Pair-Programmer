const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

export async function createRoom(language = "python") {
  const res = await fetch(`${BASE}/rooms`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ language }),
  });
  if (!res.ok) throw new Error("Failed to create room");
  return res.json();
}

export async function fetchRoom(roomId: string) {
  const res = await fetch(`${BASE}/rooms/${roomId}`);
  if (!res.ok) throw new Error("Room not found");
  return res.json();
}
