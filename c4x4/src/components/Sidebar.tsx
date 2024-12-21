import { AppProvider } from '@toolpad/core/AppProvider';
import { DashboardLayout } from '@toolpad/core/DashboardLayout';

export default function X4Base() {
  return (
    <AppProvider>
      <DashboardLayout />
    </AppProvider>
  )
}