/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { AddToBoard } from "@board/add_to_board/add_to_board";
import { patch } from "@web/core/utils/patch";


patch(AddToBoard.prototype,{
    setUp(){
        super.setUp(...arguments)
        this.notification = useService("notification");
        this.rpc = useService("rpc");
        this.state = useState({ name: this.env.config.getDisplayName() });

        useAutofocus();
    },
    addToDepartmentBoard(){
        const { domain, globalContext } = this.env.searchModel;
        const { context, groupBys, orderBy } = this.env.searchModel.getPreFavoriteValues();
        const comparison = this.env.searchModel.comparison;
        const contextToSave = {
            ...Object.fromEntries(
                Object.entries(globalContext).filter(
                    (entry) => !entry[0].startsWith("search_default_")
                )
            ),
            ...context,
            orderedBy: orderBy,
            group_by: groupBys,
            dashboard_merge_domains_contexts: false,
        };
        if (comparison) {
            contextToSave.comparison = comparison;
        }

        const result = this.rpc("/custom_dashboard/add_to_deaprtment_dashboard", {
            action_id: this.env.config.actionId || false,
            context_to_save: contextToSave,
            domain,
            name: this.state.name,
            view_mode: this.env.config.viewType,
        });

        if (result) {
            this.notification.add(
                _t("Please refresh your browser for the changes to take effect."),
                {
                    title: _t("“%s” added to dashboard", this.state.name),
                    type: "warning",
                }
            );
            this.state.name = this.env.config.getDisplayName();
        } else {
            this.notification.add(_t("Could not add filter to dashboard"), {
                type: "danger",
            });
        }
    },

    //---------------------------------------------------------------------
    // Handlers
    //---------------------------------------------------------------------
    onInputKeydownBoard(ev) {
        if (ev.key === "Enter") {
            ev.preventDefault();
            this.addToBoard();
        }
    },
    
});

