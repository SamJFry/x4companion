import FlagOutlinedIcon from '@mui/icons-material/FlagOutlined';
import PlaceOutlinedIcon from "@mui/icons-material/PlaceOutlined";
import PrecisionManufacturingOutlinedIcon from '@mui/icons-material/PrecisionManufacturingOutlined';
import FactoryOutlinedIcon from '@mui/icons-material/FactoryOutlined';
import ApartmentOutlinedIcon from '@mui/icons-material/ApartmentOutlined';
import HouseOutlinedIcon from '@mui/icons-material/HouseOutlined';
import LandslideOutlinedIcon from '@mui/icons-material/LandslideOutlined';
import { ReactRouterAppProvider } from '@toolpad/core/react-router';
import { Outlet } from 'react-router';
import type { Navigation } from '@toolpad/core';

const NAVIGATION: Navigation = [
  {kind: 'divider'},
  {
    kind: 'header',
    title: 'Empire',
  },
  {
    segment: 'x4/sectors',
    title: 'Sectors',
    icon: <FlagOutlinedIcon />
  },
  {
    segment: 'x4/stations',
    title: 'Stations',
    icon: <PlaceOutlinedIcon />
  },
  {
    segment: 'x4/factories',
    title: 'Factories',
    icon: <PrecisionManufacturingOutlinedIcon />
  },
  {
    segment: 'x4/habitats',
    title: 'Habitats',
    icon: <HouseOutlinedIcon />,
  },
  {kind: 'divider'},

  {
    kind: 'header',
    title: 'Available Modules',
  },

  {
    segment: 'x4/factory-modules',
    title: 'Factory Modules',
    icon: <FactoryOutlinedIcon />,
  },
  {
    segment: 'x4/habitat-modules',
    title: 'Habitat Modules',
    icon: <ApartmentOutlinedIcon />
  },
  {kind: 'divider'},
  {
    kind: 'header',
    title: 'Other',
  },
  {
    segment: 'x4/resources',
    title: 'Resources',
    icon: <LandslideOutlinedIcon />
  },
  {kind: 'divider'},
]

const BRANDING = {
  logo: <img src="/src/assets/X4.svg" alt="x4 logo"/>,
  title: 'Companion',
  homeUrl: 'x4',
};

export default function App() {
  return (
    <ReactRouterAppProvider navigation={NAVIGATION} branding={BRANDING}>
      <Outlet />
    </ReactRouterAppProvider>
  );
}
