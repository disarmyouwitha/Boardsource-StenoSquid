Read README.md, docs/design-review.md and draft-4/interface.json before editing. The active KiCad project is in draft-4. The owner locked the map CS P0.07, IO0 P0.21, IO3 P0.12, IO1 P0.23, CLK P0.19 and IO2 P0.05. Keep the schematic, layout, interface, validation and firmware pin states synchronized. C2 and R2 start unpopulated.

Keep every DRC category enabled. Regenerate the actual-size template after mechanical changes with tools/make_draft_d_fit_template.py. The historical tools/build_placement.py overwrites the earlier WSON layout in draft-2.

Host fit, antenna identification, Bluetooth performance and switched-rail qualification remain pending. Do not fabricate, generate production Gerbers or flash hardware without approval.
