<template>
    <div class="uk-child-width-expand@s uk-text-center uk-margin-large-top
    uk-margin-large-right uk-margin-large-left" uk-grid>
        <div>
            <div class="uk-card uk-card-default uk-card-body">
                <h3 class="uk-heading-divider">Request a ride</h3>
                <router-link class="uk-button uk-button-primary" :to="{name: 'UserApp'}">User app</router-link>
            </div>
        </div>
        <div>
            <div class="uk-card uk-card-default uk-card-body">
                <h3 class="uk-heading-divider">For drivers</h3>
                <router-link class="uk-button uk-button-primary" :to="{name: 'DriverApp'}">Driver app</router-link>
            </div>
        </div>
        <div>
            <div class="uk-card uk-card-default uk-card-body">
                <h3 class="uk-heading-divider">Super admin</h3>
                <router-link class="uk-button uk-button-primary" :to="{name: 'Dashboard'}">Dashboard</router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {

}
</script>
