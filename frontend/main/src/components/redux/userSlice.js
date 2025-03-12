import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  currentUser: null,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    signInSuccess: (state, action) => {
      state.currentUser = action.payload; // ✅ Save user data
    },
    signOut: (state) => {
      state.currentUser = null; // ✅ Clear user on logout
    },
  },
});

export const { signInSuccess, signOut } = userSlice.actions;
export default userSlice.reducer;
