import { Outlet } from 'react-router';
import { DashboardLayout } from '@toolpad/core/DashboardLayout';
import ActiveSaveProvider from '../contexts/ActiveSaveProvider.tsx';
import TopBarActions from '../components/Sidebar.tsx'

export default function Layout() {
  return (
    <ActiveSaveProvider>
      <DashboardLayout slots={{toolbarActions: TopBarActions}}>
        <Outlet />
      </DashboardLayout>
    </ActiveSaveProvider>
  );
}
