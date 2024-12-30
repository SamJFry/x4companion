import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import * as React from "react";

export default function Sectors() {
  return (
    <>
      <Box sx={{ flexGrow: 1, m: '5%', }}>
        <Typography variant="h3">Sectors</Typography>
        <Typography variant="subtitle1">
          Manage the sectors that your empire has a presence in.
        </Typography>
      </Box>
    </>
  )
}