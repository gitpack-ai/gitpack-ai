import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.scss";
import ClientLayout from './ClientLayout';

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "GitPack",
  description: "Automate Pull Request Reviews with AI",
};

const navigation = [
  { name: 'Dashboard', href: '/dashboard', current: true },
  { name: 'Pricing', href: '/pricing', current: false },
]
const userNavigation = [
  { name: 'Manage Billing', href: '/pricing' },
  { name: 'Sign out', href: '#signout' },
]

function classNames(...classes: string[]): string {
  return classes.filter(Boolean).join(' ')
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
    return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ClientLayout>{children}</ClientLayout>
      </body>
    </html>
  );
}
