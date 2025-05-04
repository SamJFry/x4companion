import {createBrowserRouter} from "react-router";
import App from "../App.tsx";
import CredentialsSignInPage from "../pages/signin.tsx";
import Layout from "../layouts/dashboard.tsx";
import Index from "../pages";
import Sectors from "../pages/sectors.tsx";
import FactoryModules from "../pages/factory-modules.tsx";

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
            path: 'factory-modules',
            Component: FactoryModules,
          }
        ],
      },
    ],
  },
]);