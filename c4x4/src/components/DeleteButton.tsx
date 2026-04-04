import * as React from "react";
import {useState} from "react";
import IconButton from "@mui/material/IconButton";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import DeleteCancelButtonPanel from "./Buttons/DeleteCancelButtonPanel.tsx";
import {Box, Modal, Typography} from "@mui/material";

const style = {
  mt: 5,
  position: 'absolute',
  top: '40%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '20%',
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
};

interface OnHoverDeleteProps {
  size?: 'small' | 'large'
  onClick: () => void
}

export function OnHoverDelete(props: OnHoverDeleteProps): React.ReactElement {
  const [isHovered, setIsHovered] = useState(false)
  const [isOpen, setOpen] = useState(false)
  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  const handleDelete = () => {
    props.onClick()
    setOpen(false)
  }

  return (
    <>
      <IconButton
        color={isHovered ? "error": "default"}
        size={props.size}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        onClick={handleOpen}
      >
        <DeleteOutlinedIcon fontSize={props.size} />
      </IconButton>
      <Modal open={isOpen} onClose={handleClose}>
        <Box sx={style}>
          <Typography sx={{mb: 2}} variant="body1">Are you sure?</Typography>
          <DeleteCancelButtonPanel deleteAction={handleDelete} cancelAction={handleClose} />
        </Box>
      </Modal>
    </>
  )
}