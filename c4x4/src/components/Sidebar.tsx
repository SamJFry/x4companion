import {AppProvider, Navigation} from '@toolpad/core/AppProvider';
import { DashboardLayout } from '@toolpad/core/DashboardLayout';
import FlagOutlinedIcon from '@mui/icons-material/FlagOutlined';
import PlaceOutlinedIcon from "@mui/icons-material/PlaceOutlined";
import PrecisionManufacturingOutlinedIcon from '@mui/icons-material/PrecisionManufacturingOutlined';
import FactoryOutlinedIcon from '@mui/icons-material/FactoryOutlined';
import ApartmentOutlinedIcon from '@mui/icons-material/ApartmentOutlined';
import HouseOutlinedIcon from '@mui/icons-material/HouseOutlined';
import LandslideOutlinedIcon from '@mui/icons-material/LandslideOutlined';
import PopupState, {bindMenu, bindTrigger} from "material-ui-popup-state";
import * as React from "react";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";

const NAVIGATION: Navigation = [
  {kind: 'divider'},

  {
    kind: 'header',
    title: 'Empire',
  },
  {
    segment: 'sectors',
    title: 'Sectors',
    icon: <FlagOutlinedIcon />
  },
  {
    segment: 'stations',
    title: 'Stations',
    icon: <PlaceOutlinedIcon />
  },
  {
    segment: 'factories',
    title: 'Factories',
    icon: <PrecisionManufacturingOutlinedIcon />
  },
  {
    segment: 'habitats',
    title: 'Habitats',
    icon: <HouseOutlinedIcon />,
  },
  {kind: 'divider'},

  {
    kind: 'header',
    title: 'Available Modules',
  },

  {
    segment: 'factory-modules',
    title: 'Factory Modules',
    icon: <FactoryOutlinedIcon />,
  },
  {
    segment: 'habitat-modules',
    title: 'Habitat Modules',
    icon: <ApartmentOutlinedIcon />
  },
  {kind: 'divider'},
  {
    kind: 'header',
    title: 'Other',
  },
  {
    segment: 'resources',
    title: 'Resources',
    icon: <LandslideOutlinedIcon />
  },
  {kind: 'divider'},
]

function ProfileDropdown() {
  return (
    <PopupState variant="popover" popupId="demo-popup-menu">
      {(popupState) => (
        <React.Fragment>
          <Button variant="contained" {...bindTrigger(popupState)}>
            Dashboard
          </Button>
          <Menu {...bindMenu(popupState)}>
            <MenuItem onClick={popupState.close}>Profile</MenuItem>
            <MenuItem onClick={popupState.close}>My account</MenuItem>
            <MenuItem onClick={popupState.close}>Logout</MenuItem>
          </Menu>
        </React.Fragment>
      )}
    </PopupState>
  );
}

export default function X4Base() {
  return (
    <AppProvider
      navigation={NAVIGATION}
      branding={{
        logo: <img src="/src/assets/X4.svg" alt="x4 logo"/>,
        title: 'Companion',
        homeUrl: '',
      }}
    >
      <DashboardLayout
        children={ProfileDropdown()}
      ></DashboardLayout>
    </AppProvider>
  )
}