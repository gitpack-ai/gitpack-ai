'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation'; // Changed from 'next/router'
import { useAuth } from '../lib/useAuth';
import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/react'
import { Bars3Icon, BellIcon, XMarkIcon } from '@heroicons/react/24/outline'
import fetchJson, {FetchError} from '../lib/fetchJson';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';

const GITHUB_APP_HANDLE = process.env.NEXT_PUBLIC_GITHUB_APP_HANDLE;

const navigation = [
  { name: 'Dashboard', href: '#', current: true },
]
const userNavigation = [
  { name: 'Sign out', href: '#' },
]

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Dashboard() {
    const auth = useAuth();
    const router = useRouter();
    const [repos, setRepos] = useState([]);

    useEffect(() => {
        if (!auth.isLoggedIn && !auth.isLoading) {
            router.push('/login');
        }
    }, [auth, router]);

    useEffect(() => {
        getGithubRepos();
    }, []);

    const logout = async () => {
        await auth.logout();
    }

    const getGithubRepos = async () => {
        try {
            const repositories = await fetchJson('/api/github/repos?is_app_installed=1');
            setRepos(repositories);
        } catch (error) {
            if (error instanceof FetchError) {
                console.error('Error fetching GitHub repositories:', error.data);
            } else {
                console.error('Error fetching GitHub repositories:', error);
            }
            // Handle the error appropriately in your UI
        }
    }

    if (!auth.isLoggedIn) {
        return "Loading..."; // Or you can return a loading indicator
    }

    return (
    <>
      <div className="min-h-full">
        <Disclosure as="nav" className="bg-gray-800">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 items-center justify-between">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <img
                    alt="Your Company"
                    src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500"
                    className="h-8 w-8"
                  />
                </div>
                <div className="hidden md:block">
                  <div className="ml-10 flex items-baseline space-x-4">
                    {navigation.map((item) => (
                      <a
                        key={item.name}
                        href={item.href}
                        aria-current={item.current ? 'page' : undefined}
                        className={classNames(
                          item.current ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white',
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
                        <MenuItem>
                            <a
                                href="#"
                                onClick={logout}
                                className="block px-4 py-2 text-sm text-gray-700 data-[focus]:bg-gray-100"
                            >
                                Sign Out
                            </a>
                        </MenuItem>
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
                  <div className="text-base font-medium leading-none text-white">{auth.user.first_name}</div>
                  <div className="text-sm font-medium leading-none text-gray-400">{auth.user.email}</div>
                </div>
              </div>
              <div className="mt-3 space-y-1 px-2">
                <DisclosureButton
                    as="a"
                    href="#"
                    onClick={logout}
                    className="block rounded-md px-3 py-2 text-base font-medium text-gray-400 hover:bg-gray-700 hover:text-white"
                >
                    Sign out
                </DisclosureButton>
              </div>
            </div>
          </DisclosurePanel>
        </Disclosure>

        <header className="bg-white shadow">
          <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold tracking-tight text-gray-900">Repositories</h1>
                <div className="mt-4 flex justify-end">
                <a
                    href={`https://github.com/apps/${process.env.NEXT_PUBLIC_GITHUB_APP_HANDLE}/installations/new`}
                    className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                    <svg className="-ml-0.5 mr-1.5 h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path d="M10.75 4.75a.75.75 0 00-1.5 0v4.5h-4.5a.75.75 0 000 1.5h4.5v4.5a.75.75 0 001.5 0v-4.5h4.5a.75.75 0 000-1.5h-4.5v-4.5z" />
                    </svg>
                    Add Repository
                </a>
                </div>
            </div>
          </div>
        </header>
        <main>
            <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
                <ul role="list" className="divide-y divide-gray-100">
                {repos.map((repo) => (
                    <li key={repo.url} className="flex justify-between gap-x-6 py-5 px-5 mb-3 rounded-lg border border-gray-200 hover:cursor-pointer hover:bg-gray-100">
                        <div className="flex min-w-0 gap-x-4">
                            <div className="min-w-0 flex-auto">
                                <p className="text-sm font-semibold leading-6 text-gray-900">{repo.full_name}</p>
                                <p className="mt-1 truncate text-xs leading-5 text-gray-500">{repo.description}</p>
                            </div>
                        </div>
                        <div className="flex items-center">
                            {!repo.private ? (
                                <div className="flex items-center">
                                    <CheckCircleIcon className="h-6 w-6 text-green-500" aria-hidden="true" />
                                </div>
                            ) : (
                                <div className="flex items-center">
                                    <XCircleIcon className="h-6 w-6 text-red-500" aria-hidden="true" />
                                </div>
                            )}
                        </div>
                    </li>
                ))}
                </ul>
          </div>
        </main>
      </div>
    </>
  )
}
