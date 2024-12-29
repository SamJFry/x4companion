import Typography from '@mui/material/Typography'
import * as React from "react";

export function SaveIndicator({ saves }) {
  if (saves.length !== 0) {
    return (
      <>
        <Typography color="primary">Save: {saves[1]["name"]}</Typography>
      </>
    )
  }
  return <></>
}