import ClientLayout from './ClientLayout';


export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
    return (
    <ClientLayout>{children}</ClientLayout>
  );
}
