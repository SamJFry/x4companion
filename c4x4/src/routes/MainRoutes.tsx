import {createBrowserRouter} from "react-router";
import App from "../App.tsx";
import CredentialsSignInPage from "../pages/signin.tsx";
import Layout from "../layouts/dashboard.tsx";
import Index from "../pages";
import Habitats from "../pages/habitats.tsx";
import HabitatModules from "../pages/habitat-modules.tsx";
import Sectors from "../pages/sectors.tsx"
import Factories from "../pages/factories.tsx"
import FactoryModules from "../pages/factory-modules.tsx";
import Stations from "../pages/stations.tsx";
import Wares from "../pages/wares.tsx";

export const router = createBrowserRouter([
  {
    Component: App, // root layout route
    children: [
      {
        path: '/',
        Component: CredentialsSignInPage
      },
      {
        path: '/x4',
        Component: Layout,
        children: [
          {
            path: '',
            Component: Index,
          },
          {
            path: 'sectors',
            Component: Sectors,
          },
          {
            path: 'stations',
            Component: Stations
          },
          {
            path: 'factories',
            Component: Factories,
          },
          {
            path: 'habitats',
            Component: Habitats,
          },
          {
            path: 'factory-modules',
            Component: FactoryModules,
          },
          {
            path: 'habitat-modules',
            Component: HabitatModules,
          },
          {
            path: 'wares',
            Component: Wares,
          }
        ],
      },
    ],
  },
]);