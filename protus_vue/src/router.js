import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/pages/HomePage";
import RegisterPage from "@/pages/UserRegisterPage";
import LoginPage from "@/pages/UserLoginPage";
import ErrorPage from "@/pages/ErrorPage";
import CompanyInfoPage from "@/pages/CompanyInfoPage";
import CustomerInfoPage from "@/pages/CustomerInfoPage";
import ConfirmPage from "@/pages/ConfirmPage";
import OAuthLoginPage from "@/pages/OAuthLoginPage";
import CompanyDashboardPage from "@/pages/CompanyDashboardPage";
import CustomerWalletPage from "@/pages/CustomerWalletPage";

const routes = [
    {
        path: '/',
        component: HomePage
    },
    {
        path: '/register',
        component: RegisterPage
    },
    {
        path: '/confirm',
        component: ConfirmPage
    },
    {
        path: '/login',
        component: LoginPage
    },
    {
        path: '/error',
        component: ErrorPage
    },
    {
        path: '/company-info',
        component: CompanyInfoPage
    },
    {
        path: '/company-dashboard',
        component: CompanyDashboardPage
    },
    {
        path: '/customer-info',
        component: CustomerInfoPage
    },
    {
        path: '/customer-wallet',
        component: CustomerWalletPage
    },
    {
        path: '/oauth-signin',
        component: OAuthLoginPage
    }
]

const router = createRouter({
    routes,
    history: createWebHistory(process.env.BASE_URL)
})

export default router;