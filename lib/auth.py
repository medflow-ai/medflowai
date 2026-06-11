"""Einfacher Passwortschutz mit EINEM gemeinsamen Passwort.

Hält Unbefugte fern, ist aber bewusst KEINE Benutzertrennung und für sich allein
nicht ausreichend für echte Patientendaten. Das Passwort wird über die
Streamlit-Secrets (APP_PASSWORD) oder die Umgebungsvariable APP_PASSWORD gesetzt –
niemals im Code.
"""
from __future__ import annotations

import hmac
import os

import streamlit as st

from lib import config as C

_AUTH_KEY = "_authed"


def _configured_password() -> str | None:
    """Liest das Passwort aus Secrets oder Umgebungsvariable – ohne zu crashen."""
    try:
        if "APP_PASSWORD" in st.secrets:
            return str(st.secrets["APP_PASSWORD"])
    except Exception:
        pass
    return os.environ.get("APP_PASSWORD")


def require_password() -> None:
    """Blockiert die App, bis das korrekte Passwort eingegeben wurde.

    Ist kein Passwort konfiguriert, bleibt die App nutzbar (mit Warnhinweis), damit
    man sich beim Deploy nicht versehentlich aussperrt.
    """
    password = _configured_password()
    if not password:
        st.warning(
            "⚠️ Kein App-Passwort gesetzt – die App ist aktuell für alle zugänglich. "
            "Zum Schützen in den Streamlit-Secrets `APP_PASSWORD` hinterlegen."
        )
        return
    if st.session_state.get(_AUTH_KEY):
        return
    _render_login(password)
    st.stop()


def _render_login(correct: str) -> None:
    st.markdown("<div style='height:7vh'></div>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        with st.container(border=True):
            st.markdown(
                "<div style='text-align:center; padding:8px 4px 0;'>"
                "<div style='font-size:2rem;'>🔒</div>"
                f"<div style='font-weight:800; font-size:1.3rem; color:#0B1F3A; margin-top:6px;'>{C.APP_NAME}</div>"
                "<div style='color:#64748B; margin-top:2px;'>Bitte Passwort eingeben, um fortzufahren.</div>"
                "</div>",
                unsafe_allow_html=True,
            )
            with st.form("mf_login", clear_on_submit=False):
                pw = st.text_input(
                    "Passwort", type="password",
                    label_visibility="collapsed", placeholder="Passwort",
                )
                ok = st.form_submit_button("Anmelden", type="primary", use_container_width=True)
            if ok:
                if hmac.compare_digest(pw or "", correct):
                    st.session_state[_AUTH_KEY] = True
                    st.rerun()
                else:
                    st.error("Falsches Passwort.")


def render_logout() -> None:
    """Kleiner Abmelden-Button in der Sidebar (nur wenn angemeldet & Passwort gesetzt)."""
    if not _configured_password() or not st.session_state.get(_AUTH_KEY):
        return
    with st.sidebar:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Abmelden", use_container_width=True, key="mf_logout"):
            st.session_state[_AUTH_KEY] = False
            st.rerun()
