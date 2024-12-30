import * as React from "react";
import {useState} from "react";
import IconButton from "@mui/material/IconButton";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";

interface OnHoverDeleteProps {
  size: 'small' | 'large'
  onClick: () => void
}

export function OnHoverDelete(props: OnHoverDeleteProps): React.ReactElement {
  const [isHovered, setIsHovered] = useState(false)
  return (
    <IconButton
      color={isHovered ? "error": "default"}
      size={props.size}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={props.onClick}
    >
      <DeleteOutlinedIcon fontSize={props.size} />
    </IconButton>
  )
}