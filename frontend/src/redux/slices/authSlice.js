import { createSlice } from "@reduxjs/toolkit";

export const initialState = {
  token: localStorage.getItem("accessToken") || null,
  user: JSON.parse(localStorage.getItem("authUser")) || null,
  lastActivityTime: Date.now(),
};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setToken: (state, action) => {
      state.token = action.payload;
      const access = action.payload;
      localStorage.setItem("accessToken", access);
      state.lastActivityTime = Date.now();
    },
    setUser: (state, action) => {
      state.user = action.payload;
      const access = JSON.stringify(action.payload);
      localStorage.setItem("authUser", access);
      state.lastActivityTime = Date.now();
    },
    resetSession: (state) => {
      state.token = null;
      state.user = null;
      localStorage.removeItem("accessToken");
      localStorage.removeItem("authUser");
    },
    RESET_LAST_ACTIVITY_TIME: (state) => {
      state.lastActivityTime = Date.now();
    },
  },
});

// Action creators are generated for each case reducer function
export const { setToken, setUser, resetSession } = authSlice.actions;

export default authSlice.reducer;
