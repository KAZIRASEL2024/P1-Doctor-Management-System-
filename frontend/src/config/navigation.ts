// Navigation configuration for the sidebar
import { LayoutDashboard, Stethoscope, Users, MapPin, Bell, Settings, PawPrint } from 'lucide-react';

export const navigationItems = [
  {
    href: '/dashboard',
    label: 'Dashboard',
    icon: LayoutDashboard,
    description: 'Overview and statistics',
  },
  {
    href: '/consultations',
    label: 'Consultations',
    icon: Stethoscope,
    description: 'Animal health case queue',
  },
  {
    href: '/doctors',
    label: 'Doctors',
    icon: Users,
    description: 'Veterinarian profiles',
  },
  {
    href: '/patients',
    label: 'Patients',
    icon: PawPrint,
    description: 'Animal patient profiles',
  },
  {
    href: '/zones',
    label: 'Zones',
    icon: MapPin,
    description: 'Geographic zone management',
  },
  {
    href: '/notifications',
    label: 'Notifications',
    icon: Bell,
    description: 'Alerts and messages',
  },
  {
    href: '/settings',
    label: 'Settings',
    icon: Settings,
    description: 'Account and system settings',
  },
] as const;
