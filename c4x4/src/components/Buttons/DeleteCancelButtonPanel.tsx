import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import DeleteIcon from '@mui/icons-material/Delete';

interface DeleteCancelButtonProps {
  deleteAction: () => void;
  cancelAction: () => void;
}

export default function DeleteCancelButtonPanel({ deleteAction, cancelAction }: DeleteCancelButtonProps) {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
      <Button onClick={cancelAction} variant="outlined" sx={{ m: 0.5 }}>Cancel</Button>
      <Button
        onClick={deleteAction}
        variant="contained"
        color="error"
        endIcon={<DeleteIcon />}
        sx={{ m: 0.5 }}>
          Confirm
      </Button>
    </Box>
  )
}