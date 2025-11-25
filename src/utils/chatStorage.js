export const STORAGE_KEY_BASE = "ps_chats_v1";

export function getStorageKey(username) {
  return username 
    ? `${STORAGE_KEY_BASE}_${username}` 
    : `${STORAGE_KEY_BASE}_guest`;
}
