import Box from "@mui/material/Box";
import Button from "@mui/material/Button";

interface AddCancelButtonProps {
  addAction: () => void;
  cancelAction: () => void;
}

export default function AddCancelButtonPanel({ addAction, cancelAction }: AddCancelButtonProps) {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
      <Button onClick={cancelAction} variant="outlined" sx={{ m: 0.5 }}>Cancel</Button>
      <Button onClick={addAction} variant="contained" sx={{ m: 0.5 }}>Add</Button>
    </Box>
  )
}