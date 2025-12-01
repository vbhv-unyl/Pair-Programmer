import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface EditorState {
  code: string;
  roomId: string | null;
  connected: boolean;
  remoteUpdate: boolean;
}

const initialState: EditorState = {
  code: "",
  roomId: null,
  connected: false,
  remoteUpdate: false,
};

const editorSlice = createSlice({
  name: "editor",
  initialState,
  reducers: {
    setCode(state, action: PayloadAction<string>) {
      state.code = action.payload;
    },
    setRoomId(state, action: PayloadAction<string>) {
      state.roomId = action.payload;
    },
    setConnected(state, action: PayloadAction<boolean>) {
      state.connected = action.payload;
    },
    setRemoteUpdate(state, action: PayloadAction<boolean>) {
      state.remoteUpdate = action.payload;
    },
  },
});

export const { setCode, setRoomId, setConnected, setRemoteUpdate } =
  editorSlice.actions;

export default editorSlice.reducer;
