import Typography from '@mui/material/Typography'
import { ActiveSaveContext } from "../contexts/ActiveSaveProvider.tsx";
import { useContext } from "react";

export function SaveIndicator() {
  const activeSave = useContext(ActiveSaveContext)
  if (activeSave.activeSave.id) {
    return <Typography color="primary">Save: {activeSave.activeSave.name}</Typography>
  }
  return <Typography color="primary"> No Saves</Typography>
}