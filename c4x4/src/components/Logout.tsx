import * as React from "react";
import {useState} from "react";
import IconButton from "@mui/material/IconButton";
import Logout from "@mui/icons-material/Logout";
import {deleteCookie} from "../functions/cookies.ts";
import {useNavigate} from "react-router";

interface OnHoverDeleteProps {
  size: 'small' | 'medium' | 'large'
  onClick: () => void
}

export function OnHoverLogout(props: OnHoverDeleteProps): React.ReactElement {
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

export default function LogOut(): React.ReactElement {
  const navigate = useNavigate()
  return <OnHoverLogout size="medium" onClick={() => {
    deleteCookie('token')
    navigate('/')
  }}/>
}