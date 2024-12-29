import * as React from "react";
import {useState} from "react";
import IconButton from "@mui/material/IconButton";
import Logout from "@mui/icons-material/Logout";

interface OnHoverDeleteProps {
  size: 'small' | 'medium' | 'large'
  onClick: () => void
}

export default function OnHoverLogout(props: OnHoverDeleteProps): React.ReactElement {
  const [isHovered, setIsHovered] = useState(false)
  return (
    <IconButton
      color={isHovered ? "error": "default"}
      size={props.size}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={props.onClick}
    >
      <Logout fontSize={props.size} />
    </IconButton>
  )
}