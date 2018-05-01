<template>
    <div>
        <GlobalNavBar />
        <div class="uk-child-width-3@s uk-child-width-1-3@m uk-padding" uk-grid>
            <div v-if="!$route.params['driver_id']">
                Please select a driver:
                <select class="uk-select" v-model="selected_driver" v-on:change="set_driver">
                    <option selected disabled>Select a driver</option>
                    <option v-for="driver in available_drivers" :value="driver.id" :key="driver.id">
                        {{ driver.name }}
                    </option>
                </select>
            </div>
            <div v-else>
                <ul class="uk-breadcrumb">
                    <li>
                        <router-link :to="{name: $route.name, params: {}}">
                            Drivers
                        </router-link>
                    </li>
                    <li><span> {{ driver_name }} </span></li>
                </ul>
                <ul class="uk-child-width-expand uk-subnav" uk-tab>
                    <li class="uk-active"><a href="#ongoing">Ongoing</a></li>
                    <li><a href="#waiting">Waiting</a></li>
                    <li><a href="#complete">Complete</a></li>
                </ul>

                <ul class="uk-switcher uk-margin">
                    <li>
                        <a @click="fetch_ongoing_ride()" class="uk-text-center">Refresh</a>                            
                        <div class="uk-section uk-section-muted" v-if="fetching_ongoing_ride">
                            <div class="uk-text-center uk-margin-large-top uk-margin-large-bottom" v-if="fetching_ongoing_ride">
                                <div uk-spinner></div><br>
                                <div class="uk-margin-small-right">Fetching your current ride details..</div>
                            </div>
                        </div>
                        <div class="uk-section uk-section-muted" v-else>
                            <div class="uk-container uk-text-center" v-if="ongoing_ride">
                                Ride ID: # {{ ongoing_ride.id }} <br>
                                User ID: # {{ ongoing_ride.user }} <br>
                                Requested at: {{ ongoing_ride.created_at }} <br>
                                Picked up at: {{ ongoing_ride.modified_at }}
                            </div>
                            <div class="uk-container uk-text-center" v-else>
                                You do not appear to be on any active rides. <br>
                                Pickup a ride from the <code>Waiting</code> tab.
                            </div>
                        </div>
                    </li>
                    <li>
                        <a @click="fetch_waiting_rides()" class="uk-text-center">Refresh</a>                                                    
                        <div class="uk-section uk-section-muted uk-text-center uk-margin-large-top uk-margin-large-bottom" v-if="fetching_waiting_rides">
                            <div uk-spinner></div><br>
                            <div class="uk-margin-small-right">Fetching your pending rides..</div>
                        </div>
                        <div v-else>
                            <table class="uk-table uk-table-hover uk-table-middle uk-table-small" v-if="waiting_rides.length > 0">
                                <tbody>
                                    <tr v-for="ride in waiting_rides" :key="ride.id">
                                        <td># {{ ride.id }}</td>
                                        <td class="uk-text-right">
                                            <button class="uk-button uk-button-default" @click="pickup_ride(ride)">
                                                Pickup
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <div class="uk-section uk-section-muted" v-else>
                                <div class="uk-container uk-text-center">
                                    Currently there are no waiting rides. <br>
                                    Check back after some time..
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <a class="uk-text-center" @click="fetch_completed_rides()">Refresh</a>
                        <div class="uk-section uk-section-muted uk-text-center uk-margin-large-top uk-margin-large-bottom" v-if="fetching_completed_rides">
                            <div uk-spinner></div><br>
                            <div class="uk-margin-small-right">Loading your completed rides..</div>
                        </div>
                        <div v-else>
                            <div class="uk-section uk-section-muted uk-container uk-text-center" 
                                v-if="completed_rides.length==0">
                                You have not completed any rides yet.. <br>
                                Your completed rides appear here.
                            </div>
                            <table class="uk-table uk-table-hover uk-table-middle" v-else>
                                <tbody>
                                    <tr>
                                        <td># 12312</td>
                                        <td class="uk-text-right">12:46:39 PM</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            waiting_rides: [],
            ongoing_ride: null,
            completed_rides: [],
            selected_driver: 'Select a driver',
            available_drivers: [
                {
                    id: 1,
                    name: 'Driver 1'
                }, {
                    id: 2,
                    name: 'Driver 2'
                }, {
                    id: 3,
                    name: 'Driver 3'
                }, {
                    id: 4,
                    name: 'Driver 4'
                }, {
                    id: 5,
                    name: 'Driver 5'
                }, 
            ],
            fetching_waiting_rides: false,
            fetching_ongoing_ride: false,
            fetching_completed_rides: false,
            fetching_driver_list: false
        }
    },
    computed: {
        driver_name () {
            return "Driver " + this.$route.params['driver_id']
        }
    },
    methods: {
        pickup_ride (ride) {
            this.$http.post('/api/driver/pickup/', {
                'driver_id': this.$route.params['driver_id'],
                'ride_id': ride.id
            }).then( successResponse => {
                this.waiting_rides.splice(this.waiting_rides.indexOf(ride), 1);
            }, errorResponse => {
                UIkit.notification({
                    message: errorResponse.body.message,
                    status: 'danger',
                    pos: 'bottom-center',
                    timeout: 5000
                })
                /* if(errorResponse.status === 404){
                    this.waiting_rides.splice(this.waiting_rides.indexOf(ride), 1);
                    
                } */
                // If status code == 404:
                // delete the ride object from the list, and show a notification
            })
        },
        fetch_waiting_rides () {
            this.fetching_waiting_rides = true;
            this.$http.get('/api/driver/waiting_rides/').then(successResponse => {
                this.waiting_rides = successResponse.data.waiting_rides;
                this.fetching_waiting_rides = false;
            }, errorResponse => {
                this.fetching_waiting_rides = false;
            })
        },
        fetch_completed_rides () {
            this.fetching_completed_rides = true;
            this.$http.get('/api/driver/completed_rides/?driver_id=' + this.$route.params['driver_id']).then(
                successResponse => {
                    this.completed_rides = successResponse.data.completed_rides;
                    this.fetching_completed_rides = false;
                }, errorResponse => {
                    this.fetching_completed_rides = false;
                })
        },
        fetch_ongoing_ride () {
            this.fetching_ongoing_ride = true;
            this.$http.get('/api/driver/ongoing_ride/?driver_id=' + this.$route.params['driver_id']).then(
                successResponse => {
                    this.ongoing_ride = successResponse.data.ride_details;
                    this.fetching_ongoing_ride = false;
                }, 
                errorResponse => {
                    this.fetching_ongoing_ride = false
                }
            )
        },
        set_driver () {
            this.$router.push({name: this.$route.name, params: {driver_id: this.selected_driver}});
        },
        fetch_init_data () {
            this.fetch_ongoing_ride();
            this.fetch_waiting_rides();
            this.fetch_completed_rides();
        }
    },
    mounted () {
        if(typeof( this.$route.params.driver_id ) !== "undefined") {
            this.fetch_init_data();
            /* const vm = this;
            $('.uk-switcher').on('show.uk.switcher', function(event, area){
                vm.fetch_init_data();
            }); */
        }
    }
}
</script>
