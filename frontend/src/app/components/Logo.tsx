const LogoComponent = (props: { className?: string, isLight: boolean }) => {
    return (
    <>
        {props.isLight ? (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            xmlnsXlink="http://www.w3.org/1999/xlink"
            width={1}
            viewBox="0 0 64 64"
            {...props}
        >
            <defs>
            <linearGradient id="a">
                <stop
                offset={0}
                style={{
                    stopColor: "#fcfcfc",
                }}
                />
                <stop
                offset={1}
                style={{
                    stopColor: "rgba(215,215,215,.9)",
                }}
                />
            </linearGradient>
            <linearGradient
                xlinkHref="#a"
                id="b"
                x1={54.5}
                x2={54.5}
                y1={35.914}
                y2={49}
                gradientUnits="userSpaceOnUse"
            />
            <linearGradient
                xlinkHref="#a"
                id="c"
                x1={9.5}
                x2={9.5}
                y1={35.914}
                y2={49}
                gradientUnits="userSpaceOnUse"
            />
            <linearGradient
                xlinkHref="#a"
                id="d"
                x1={32}
                x2={32}
                y1={19}
                y2={49}
                gradientUnits="userSpaceOnUse"
            />
            <linearGradient
                xlinkHref="#a"
                id="e"
                x1={22}
                x2={22}
                y1={11}
                y2={53}
                gradientUnits="userSpaceOnUse"
            />
            <linearGradient
                xlinkHref="#a"
                id="f"
                x1={42}
                x2={42}
                y1={11}
                y2={53}
                gradientUnits="userSpaceOnUse"
            />
            </defs>
            <g>
            <path
                d="M49 35.914V49h11v-3.001L49 35.914z"
                style={{
                paintOrder: "stroke",
                fill: "url(#b)",
                }}
                transform="matrix(.85714 0 0 .84573 5.028 5.615)"
            />
            <path
                d="M15 35.914 4 45.999V49h11V35.914z"
                style={{
                paintOrder: "stroke",
                fill: "url(#c)",
                }}
                transform="matrix(.85714 0 0 .84573 5.028 5.615)"
            />
            <path
                d="M32 19c-1.162 0-2.295.095-3.377.269l.003.018c.248 1.495.374 3.054.374 4.633V49h6V23.92c0-1.572.126-3.128.374-4.624l.004-.022A20.842 20.842 0 0 0 32 19Z"
                style={{
                paintOrder: "stroke",
                fill: "url(#d)",
                }}
                transform="matrix(.85714 0 0 .84573 5.028 5.615)"
            />
            <path
                d="M27.64 19.45h-.01C26.79 14.51 24.59 11 22 11c-3.32 0-6 5.78-6 12.92V53h3.5v-9.9c0-.17.224-.308.5-.308s.5.138.5.308V53H28V23.92c0-1.57-.13-3.08-.36-4.47z"
                style={{
                paintOrder: "stroke",
                fill: "url(#e)",
                }}
                transform="matrix(.85714 0 0 .84573 5.028 5.615)"
            />
            <path
                d="M42 11c-2.59 0-4.79 3.52-5.64 8.46-.23 1.39-.36 2.89-.36 4.46V53h7.5v-9.9c0-.17.224-.308.5-.308s.5.138.5.308V53H48V23.92C48 16.78 45.32 11 42 11z"
                style={{
                paintOrder: "stroke",
                fill: "url(#f)",
                }}
                transform="matrix(.85714 0 0 .84573 5.028 5.615)"
            />
            </g>
        </svg>) : (
            <svg className={props.className} version="1.1" x="0" y="0" viewBox="0 0 64 64" enableBackground="new 0 0 64 64" width="1px" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink">
            <defs>
                <linearGradient id="gradient-5">
                    <stop offset="0" stopColor="rgb(126, 126, 218)" />
                    <stop offset="1" stopColor="rgb(22, 28, 117)" />
                </linearGradient>
                <linearGradient id="gradient-5-0" gradientUnits="userSpaceOnUse" x1="54.5" y1="35.914" x2="54.5" y2="49" xlinkHref="#gradient-5" />
                <linearGradient id="gradient-5-1" gradientUnits="userSpaceOnUse" x1="9.5" y1="35.914" x2="9.5" y2="49" xlinkHref="#gradient-5" />
                <linearGradient id="gradient-5-2" gradientUnits="userSpaceOnUse" x1="32" y1="19" x2="32" y2="49" xlinkHref="#gradient-5" />
                <linearGradient id="gradient-5-3" gradientUnits="userSpaceOnUse" x1="22" y1="11" x2="22" y2="53" xlinkHref="#gradient-5" />
                <linearGradient id="gradient-5-4" gradientUnits="userSpaceOnUse" x1="42" y1="11" x2="42" y2="53" xlinkHref="#gradient-5" />
            </defs>
            <g transform="matrix(0.857143, 0, 0, 0.845732, 5.028159, 5.614667)">
                <path d="M49,35.914V49h11c0,0,0-1,0-3.001L49,35.914z" style={{paintOrder: "stroke", fill: "url(#gradient-5-0)"}} />
                <path d="M15,35.914L4,45.999C4,48,4,49,4,49h11V35.914z" style={{paintOrder: "stroke", fill: "url(#gradient-5-1)"}} />
                <path d="M 32 19 C 30.838 19 29.705 19.095 28.623 19.269 L 28.626 19.287 C 28.874 20.782 29 22.341 29 23.92 L 29 49 L 35 49 L 35 23.92 C 35 22.348 35.126 20.792 35.374 19.296 C 35.375 19.288 35.377 19.281 35.378 19.274 C 34.296 19.096 33.163 19 32 19 Z" style={{paintOrder: "stroke", fill: "url(#gradient-5-2)"}} />
                <path d="M27.64,19.45h-0.01C26.79,14.51,24.59,11,22,11c-3.32,0-6,5.78-6,12.92V53h3.5v-9.9c0-0.17,0.224-0.308,0.5-0.308   s0.5,0.138,0.5,0.308V53H28V23.92C28,22.35,27.87,20.84,27.64,19.45z" style={{paintOrder: "stroke", fill: "url(#gradient-5-3)"}} />
                <path d="M42,11c-2.59,0-4.79,3.52-5.64,8.46C36.13,20.85,36,22.35,36,23.92V53h7.5v-9.9c0-0.17,0.224-0.308,0.5-0.308   s0.5,0.138,0.5,0.308V53H48V23.92C48,16.78,45.32,11,42,11z" style={{paintOrder: "stroke", fill: "url(#gradient-5-4)"}} />
            </g>
        </svg>
        )}
    </>
    );
}

export default LogoComponent;