'use client';

import { useAuth } from '../lib/useAuth';
import { useUser } from '../components/ProtectedRoute';
import { useRouter, usePathname } from 'next/navigation';
import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/react';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import LogoComponent from '../components/Logo';


const navigation = [
  { name: 'Repositories', href: '/repositories' },
  { name: 'Pricing', href: '/pricing' },
]
const userNavigation = [
  { name: 'Manage Billing', href: '/pricing' },
  { name: 'Sign out', href: '#signout' },
]

function classNames(...classes: string[]): string {
  return classes.filter(Boolean).join(' ')
}

export default function ClientLayout({
    children,
  }: Readonly<{
    children: React.ReactNode;
  }>) {
  const auth = useAuth();
  const user = useUser();
  const router = useRouter();
  const pathname = usePathname();

  const signout = () => {
    auth.logout();
    router.push('/');
  }

  return (
    <div className="min-h-full">
        <Disclosure as="nav" className="bg-gray-800">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 items-center justify-between">
                <div className="flex items-center">
                <div className="flex-shrink-0">
                    <a href='/repositories'>
                        <LogoComponent light="true" className="h-10 w-10 text-white" />
                    </a>
                </div>
                <div className="hidden md:block">
                    <div className="ml-10 flex items-baseline space-x-4">
                    {navigation.map((item) => (
                        <a
                        key={item.name}
                        href={item.href}
                        aria-current={pathname === item.href ? 'page' : undefined}
                        className={classNames(
                             item.href === pathname ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white',
                            'rounded-md px-3 py-2 text-sm font-medium',
                        )}
                        >
                        {item.name}
                        </a>
                    ))}
                    </div>
                </div>
                </div>
                <div className="hidden md:block">
                <div className="ml-4 flex items-center md:ml-6">
                    {/* Profile dropdown */}
                    <Menu as="div" className="relative ml-3">
                    <div>
                        <MenuButton className="relative flex max-w-xs items-center rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                        <span className="absolute -inset-1.5" />
                        <span className="sr-only">Open user menu</span>
                        <svg className="h-10 w-10 rounded-full text-gray-300" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                            <path fillRule="evenodd" d="M18.685 19.097A9.723 9.723 0 0021.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 003.065 7.097A9.716 9.716 0 0012 21.75a9.716 9.716 0 006.685-2.653zm-12.54-1.285A7.486 7.486 0 0112 15a7.486 7.486 0 015.855 2.812A8.224 8.224 0 0112 20.25a8.224 8.224 0 01-5.855-2.438zM15.75 9a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" clipRule="evenodd" />
                        </svg>
                        </MenuButton>
                    </div>
                    <MenuItems
                        transition
                        className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 transition focus:outline-none data-[closed]:scale-95 data-[closed]:transform data-[closed]:opacity-0 data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
                    >
                        {userNavigation.map((item) => (
                            <MenuItem key={item.name} as="div">
                                {() => (
                                    <a
                                        href={item.href}
                                        onClick={item.href === '#signout' ? signout : undefined}
                                        className={`block px-4 py-2 text-sm text-gray-700 `}
                                    >
                                        {item.name}
                                    </a>
                                )}
                            </MenuItem>
                        ))}
                    </MenuItems>
                    </Menu>
                </div>
                </div>
                <div className="-mr-2 flex md:hidden">
                {/* Mobile menu button */}
                <DisclosureButton className="group relative inline-flex items-center justify-center rounded-md bg-gray-800 p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                    <span className="absolute -inset-0.5" />
                    <span className="sr-only">Open main menu</span>
                    <Bars3Icon aria-hidden="true" className="block h-6 w-6 group-data-[open]:hidden" />
                    <XMarkIcon aria-hidden="true" className="hidden h-6 w-6 group-data-[open]:block" />
                </DisclosureButton>
                </div>
            </div>
            </div>

            <DisclosurePanel className="md:hidden">
            <div className="space-y-1 px-2 pb-3 pt-2 sm:px-3">
                {navigation.map((item) => (
                <DisclosureButton
                    key={item.name}
                    as="a"
                    href={item.href}
                    aria-current={item.current ? 'page' : undefined}
                    className={classNames(
                    item.current ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white',
                    'block rounded-md px-3 py-2 text-base font-medium',
                    )}
                >
                    {item.name}
                </DisclosureButton>
                ))}
            </div>
            <div className="border-t border-gray-700 pb-3 pt-4">
                <div className="flex items-center px-5">
                <div className="flex-shrink-0">
                    <svg className="h-10 w-10 rounded-full text-gray-300" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                    <path fillRule="evenodd" d="M18.685 19.097A9.723 9.723 0 0021.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 003.065 7.097A9.716 9.716 0 0012 21.75a9.716 9.716 0 006.685-2.653zm-12.54-1.285A7.486 7.486 0 0112 15a7.486 7.486 0 015.855 2.812A8.224 8.224 0 0112 20.25a8.224 8.224 0 01-5.855-2.438zM15.75 9a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" clipRule="evenodd" />
                    </svg>
                </div>
                <div className="ml-3">
                    <div className="text-base font-medium leading-none text-white">{user ? user.first_name : ''}</div>
                    <div className="text-sm font-medium leading-none text-gray-400">{user ? user.email : ''}</div>
                </div>
                </div>
                <div className="mt-3 space-y-1 px-2">
                <DisclosureButton
                    as="a"
                    href="#"
                    onClick={signout}
                    className="block rounded-md px-3 py-2 text-base font-medium text-gray-400 hover:bg-gray-700 hover:text-white"
                >
                    Sign out
                </DisclosureButton>
                </div>
            </div>
            </DisclosurePanel>
        </Disclosure>
        {children}
    </div>
  );
}
