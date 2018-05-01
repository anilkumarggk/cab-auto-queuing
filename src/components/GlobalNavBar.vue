<template lang="html">
    <div>
        <div uk-sticky="sel-target: .uk-navbar-container; cls-active: uk-navbar-sticky; bottom: #transparent-sticky-navbar">
            <nav class="uk-navbar-container" uk-navbar style="position: relative; z-index: 980;">
                <div class="uk-navbar-center">
                    <ul class="uk-navbar-nav">
                        <li v-for="nav_route in nav_routes" :class="{'uk-active': $route.name===nav_route.name}">
                            <router-link :to="{ name: nav_route.name }">{{ nav_route.nav.title }}</router-link>
                        </li>
                    </ul>
                </div>
            </nav>
        </div>
    </div>
</template>

<script>
export default {
    computed: {
        nav_routes () {
            return this.$router.options.routes.filter(route => {
                try {
                    return route['nav']['visible']
                } catch (err) {
                    return false
                }
            })
        }
    }
}
</script>
