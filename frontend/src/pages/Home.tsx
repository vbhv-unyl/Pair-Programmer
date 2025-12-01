import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createRoom } from "../utils/api";

export default function Home() {
  const [joinId, setJoinId] = useState("");
  const [loading, setLoading] = useState(false);
  const nav = useNavigate();

  const onCreate = async () => {
    setLoading(true);
    try {
      const data = await createRoom("python");
      nav(`/room/${data.room_id}`);
    } catch (e) {
      alert("Create failed");
    } finally {
      setLoading(false);
    }
  };

  const onJoin = () => {
    if (!joinId.trim()) {
      alert("Enter room id");
      return;
    }
    nav(`/room/${joinId.trim()}`);
  };

  return (
    <div className="app-shell">
      <div className="header">
        <div><strong>PairProg</strong></div>
      </div>
      <div className="container">
        <h2>Create or Join Room</h2>
        <div style={{ marginBottom: 12 }}>
          <button className="btn" onClick={onCreate} disabled={loading}>
            {loading ? "Creating..." : "Create New Room"}
          </button>
        </div>

        <div>
          <input
            placeholder="Enter room id"
            className="input"
            value={joinId}
            onChange={(e) => setJoinId(e.target.value)}
          />
          <button className="btn" style={{ marginLeft: 8 }} onClick={onJoin}>
            Join
          </button>
        </div>

        <p className="small" style={{ marginTop: 12 }}>
          Tip: open two windows and join the same room id to test real-time sync.
        </p>
      </div>
    </div>
  );
}
