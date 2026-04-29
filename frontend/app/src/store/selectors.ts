import type { RootState } from "./store";

export const selectIsGlobalLoading = (state: RootState) =>
  state.auth.loading
