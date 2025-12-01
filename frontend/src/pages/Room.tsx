import React, { useEffect, useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../store/hooks";
import { setCode, setRoomId, setConnected } from "../store/slices/editorSlice";
import { fetchRoom } from "../utils/api";
import { WSClient } from "../utils/wsClient";
import CodeEditor from "../components/Editor";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../store";

import debounce from "lodash.debounce";

export default function RoomPage() {
  const { roomId } = useParams<{ roomId: string }>();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const code = useSelector((s: RootState) => s.editor.code);

  const wsRef = useRef<WSClient | null>(null);
  const [status, setStatus] = useState("connecting");

  // initialize room: fetch code, connect ws
  useEffect(() => {
    if (!roomId) {
      navigate("/");
      return;
    }
    (async () => {
      try {
        const data = await fetchRoom(roomId);
        dispatch(setRoomId(data.room_id));
        dispatch(setCode(data.code || ""));
      } catch (e) {
        alert("Room not found");
        navigate("/");
      }
    })();
  }, [roomId]);

  // connect websocket
  useEffect(() => {
    if (!roomId) return;
    const client = new WSClient(roomId, (msg) => {
      if (msg.type === "sync" || msg.type === "update" || msg.type === "code_change") {
        // many backends use different names — accept common ones
        if (msg.code !== undefined) {
          dispatch(setCode(msg.code));
        }
      }
    });
    wsRef.current = client;
    client.connect();
    setStatus("connected");
    dispatch(setConnected(true));

    return () => {
      client.close();
      setStatus("disconnected");
      dispatch(setConnected(false));
    };
  }, [roomId]);

  // debounced send
  // note: backend expects messages of type "code_change"
  const sendChange = useRef(
    debounce((newCode: string) => {
      wsRef.current?.send({ type: "code_change", code: newCode });
    }, 300)
  ).current;

  const onChange = (newCode: string) => {
    dispatch(setCode(newCode));
    sendChange(newCode);
  };

  return (
    <div className="app-shell">
      <div className="header">
        <div>
          <strong>PairProg</strong> — Room <span style={{ color: "#ef4444" }}>{roomId}</span>
        </div>
        <div>
          <span className="small">Status: {status}</span>
        </div>
      </div>

      <div className="container">
        <div style={{ marginBottom: 12 }}>
          <button className="btn" onClick={() => navigate("/")}>
            Back
          </button>
        </div>

        <CodeEditor value={code} onChange={onChange} language={"python"} />
      </div>
    </div>
  );
}
