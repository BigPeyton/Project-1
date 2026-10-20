# Development validation run

AI-assisted development audit; NOT a recorded fresh-environment cold run or human AI-off exercise.

- Started (UTC): 2026-10-20T02:16:29.745456+00:00
- Elapsed: 3.003532 seconds
- Python: 3.13.15 (tags/v3.13.15:4061bc4, Aug  5 2026, 13:05:39) [MSC v.1944 64 bit (AMD64)]
- Platform: Windows-11-10.0.26300-SP0
- Source/data/tests SHA256 fingerprint: `fa90591f1c57c972fd0253ab8546d0cee7f7d247dd7f75408e2dfcae75f087c9`
- Tests: 105; successful: True
- Overall pass: True
- First unexpected failure in this run: none

## Saved-output reproduction

- valuation-transition: PASS. JSON and Markdown exactly reproduce.
- equity-bridge: PASS. JSON and Markdown exactly reproduce.
- downside-exit: PASS. JSON and Markdown exactly reproduce.
- comparables: PASS. JSON and Markdown exactly reproduce.
- reverse-dcf: PASS. JSON and Markdown exactly reproduce.
- proforma-sensitivity: PASS. JSON and Markdown exactly reproduce.

## Highest-risk development probe

PASS: expected funding failure observed. 2030: additional external funding of 314.688 million required; no committed facility assumed.
Continuing downside cannot be underwritten without committed funding; WATCH can become DO NOT INITIATE. Separate exit remains conditional.

This probes funding failure; it does not prove terminal assumptions, transaction scope or recovery values. Prior development failures remain recorded in docs/reverse-dcf-validation.md and the other validation notes. No first failure or elapsed time from a separate cold run is inferred here.

## Must fix before submission

- Student AI-off locked prediction AND execution, with precommit evidence
- Recorded README-only fresh-environment cold run with first failure and elapsed time
- Final PDFs, three real videos and corrected timestamped transcripts
- Manifest, source/access review, version freeze and submission receipt

## Executed tests

```text
test_boundary_failure_then_recovery (test_app.ApplicationTests.test_boundary_failure_then_recovery) ... ok
test_change_then_reset_no_file_mutation (test_app.ApplicationTests.test_change_then_reset_no_file_mutation) ... ok
test_downside_funding_not_hidden (test_app.ApplicationTests.test_downside_funding_not_hidden) ... ok
test_export_uses_same_inputs_and_escapes_reflected_text (test_app.ApplicationTests.test_export_uses_same_inputs_and_escapes_reflected_text) ... ok
test_invalid_and_duplicate_parameters (test_app.ApplicationTests.test_invalid_and_duplicate_parameters) ... ok
test_only_allowlisted_evidence_is_served (test_app.ApplicationTests.test_only_allowlisted_evidence_is_served) ... ok
test_page_exposes_statement_and_scope_evidence (test_app.ApplicationTests.test_page_exposes_statement_and_scope_evidence) ... ok
test_reference_matches_saved_financial_engine (test_app.ApplicationTests.test_reference_matches_saved_financial_engine) ... ok
test_live_export_and_headers (test_app.LiveHTTPTests.test_live_export_and_headers) ... ok
test_live_failure_then_success (test_app.LiveHTTPTests.test_live_failure_then_success) ... ok
test_financing_pairs_shares_with_net_proceeds (test_cash_bridge.CashBridgeTests.test_financing_pairs_shares_with_net_proceeds) ... ok
test_invalid_inputs_fail_loudly (test_cash_bridge.CashBridgeTests.test_invalid_inputs_fail_loudly) ... ok
test_no_burn_cash_excludes_restricted_and_unused_funding (test_cash_bridge.CashBridgeTests.test_no_burn_cash_excludes_restricted_and_unused_funding) ... ok
test_option_proceeds_not_counted_twice (test_cash_bridge.CashBridgeTests.test_option_proceeds_not_counted_twice) ... ok
test_portfolio_transfer_preserves_liquidity (test_cash_bridge.CashBridgeTests.test_portfolio_transfer_preserves_liquidity) ... ok
test_stress_lowers_available_liquidity (test_cash_bridge.CashBridgeTests.test_stress_lowers_available_liquidity) ... ok
test_claims_do_not_subtract_undrawn_commitment_or_operating_leases (test_claims_bridge.ClaimsTests.test_claims_do_not_subtract_undrawn_commitment_or_operating_leases) ... ok
test_conversion_exchanges_claim_for_shares (test_claims_bridge.ClaimsTests.test_conversion_exchanges_claim_for_shares) ... ok
test_earnout_rollforward_rejects_missing_addition (test_claims_bridge.ClaimsTests.test_earnout_rollforward_rejects_missing_addition) ... ok
test_lease_principal_payment_reduces_cash_and_claim_equally (test_claims_bridge.ClaimsTests.test_lease_principal_payment_reduces_cash_and_claim_equally) ... ok
test_currency_scale_invariance (test_downside_and_comparables.ComparableTests.test_currency_scale_invariance) ... ok
test_duplicates_bad_denominator_and_treasury_shares (test_downside_and_comparables.ComparableTests.test_duplicates_bad_denominator_and_treasury_shares) ... ok
test_equity_and_ev_definitions_reconcile (test_downside_and_comparables.ComparableTests.test_equity_and_ev_definitions_reconcile) ... ok
test_leave_one_out_does_not_invent_a_range (test_downside_and_comparables.ComparableTests.test_leave_one_out_does_not_invent_a_range) ... ok
test_less_excess_peer_cash_increases_ev_not_ps (test_downside_and_comparables.ComparableTests.test_less_excess_peer_cash_increases_ev_not_ps) ... ok
test_no_future_same_day_unknown_or_currency_mismatch (test_downside_and_comparables.ComparableTests.test_no_future_same_day_unknown_or_currency_mismatch) ... ok
test_ps_does_not_receive_a_second_cash_bridge (test_downside_and_comparables.ComparableTests.test_ps_does_not_receive_a_second_cash_bridge) ... ok
test_insolvent_exit_fails_loudly (test_downside_and_comparables.DownsideTests.test_insolvent_exit_fails_loudly) ... ok
test_no_cash_double_recovery (test_downside_and_comparables.DownsideTests.test_no_cash_double_recovery) ... ok
test_no_claim_double_settlement (test_downside_and_comparables.DownsideTests.test_no_claim_double_settlement) ... ok
test_recovery_and_closure_cost_direction (test_downside_and_comparables.DownsideTests.test_recovery_and_closure_cost_direction) ... ok
test_reserve_release_and_option_warning (test_downside_and_comparables.DownsideTests.test_reserve_release_and_option_warning) ... ok
test_stop_before_failure_without_new_funding (test_downside_and_comparables.DownsideTests.test_stop_before_failure_without_new_funding) ... ok
test_truncation_preserves_prior_cashflows (test_downside_and_comparables.DownsideTests.test_truncation_preserves_prior_cashflows) ... ok
test_bad_amounts_fail (test_equity_bridge.EquityBridgeTests.test_bad_amounts_fail) ... ok
test_cash_change_has_dollar_for_dollar_effect (test_equity_bridge.EquityBridgeTests.test_cash_change_has_dollar_for_dollar_effect) ... ok
test_claim_reconciliation_and_input_preservation (test_equity_bridge.EquityBridgeTests.test_claim_reconciliation_and_input_preservation) ... ok
test_customer_recovery_and_reserve_direction (test_equity_bridge.EquityBridgeTests.test_customer_recovery_and_reserve_direction) ... ok
test_fair_price_issuance_neutral_before_fees (test_equity_bridge.EquityBridgeTests.test_fair_price_issuance_neutral_before_fees) ... ok
test_financing_must_pair_cash_and_shares (test_equity_bridge.EquityBridgeTests.test_financing_must_pair_cash_and_shares) ... ok
test_future_cash_is_discounted_but_shares_are_not (test_equity_bridge.EquityBridgeTests.test_future_cash_is_discounted_but_shares_are_not) ... ok
test_integrated_numerator_and_share_count (test_equity_bridge.EquityBridgeTests.test_integrated_numerator_and_share_count) ... ok
test_intrinsic_note_and_option_election (test_equity_bridge.EquityBridgeTests.test_intrinsic_note_and_option_election) ... ok
test_known_option_cash_not_added_twice (test_equity_bridge.EquityBridgeTests.test_known_option_cash_not_added_twice) ... ok
test_limited_liability_displays_shortfall (test_equity_bridge.EquityBridgeTests.test_limited_liability_displays_shortfall) ... ok
test_mismatch_and_conditional_funding_rejected (test_equity_bridge.EquityBridgeTests.test_mismatch_and_conditional_funding_rejected) ... ok
test_note_claim_and_conversion_exclusive (test_equity_bridge.EquityBridgeTests.test_note_claim_and_conversion_exclusive) ... ok
test_payment_before_cutoff_removes_cash_and_claim_once (test_equity_bridge.EquityBridgeTests.test_payment_before_cutoff_removes_cash_and_claim_once) ... ok
test_duplicate_and_post_cutoff_evidence_rejected (test_normalization.NormalizationTests.test_duplicate_and_post_cutoff_evidence_rejected) ... ok
test_noncash_removal_cannot_create_cash (test_normalization.NormalizationTests.test_noncash_removal_cannot_create_cash) ... ok
test_reconciliation_and_reported_data_preserved (test_normalization.NormalizationTests.test_reconciliation_and_reported_data_preserved) ... ok
test_wrong_da_scope_fails (test_normalization.NormalizationTests.test_wrong_da_scope_fails) ... ok
test_bad_units_values_and_cutoff_fail (test_operating_forecast.OperatingTests.test_bad_units_values_and_cutoff_fail) ... ok
test_guidance_is_an_anchor_not_a_constraint_on_downside (test_operating_forecast.OperatingTests.test_guidance_is_an_anchor_not_a_constraint_on_downside) ... ok
test_margin_change_flows_to_gross_profit_and_ebit_once (test_operating_forecast.OperatingTests.test_margin_change_flows_to_gross_profit_and_ebit_once) ... ok
test_rd_increase_reduces_ebit_dollar_for_dollar (test_operating_forecast.OperatingTests.test_rd_increase_reduces_ebit_dollar_for_dollar) ... ok
test_reported_history_and_normalized_view_stay_separate (test_operating_forecast.OperatingTests.test_reported_history_and_normalized_view_stay_separate) ... ok
test_zero_neutron_does_not_erase_readiness_or_rd (test_operating_forecast.OperatingTests.test_zero_neutron_does_not_erase_readiness_or_rd) ... ok
test_app_operating_change_flows_through_all_statements_and_reset (test_proforma_sensitivity.OperatingSensitivityTests.test_app_operating_change_flows_through_all_statements_and_reset) ... ok
test_bounds_fail_loudly (test_proforma_sensitivity.OperatingSensitivityTests.test_bounds_fail_loudly) ... ok
test_defaults_preserve_model_and_source (test_proforma_sensitivity.OperatingSensitivityTests.test_defaults_preserve_model_and_source) ... ok
test_growth_change_compounds_four_years_only (test_proforma_sensitivity.OperatingSensitivityTests.test_growth_change_compounds_four_years_only) ... ok
test_neutron_scale_preserves_fixed_costs (test_proforma_sensitivity.OperatingSensitivityTests.test_neutron_scale_preserves_fixed_costs) ... ok
test_rankings_use_actual_endpoint_spans_and_alternative_ranges (test_proforma_sensitivity.OperatingSensitivityTests.test_rankings_use_actual_endpoint_spans_and_alternative_ranges) ... ok
test_rd_change_known_ebit_effect_and_no_historical_change (test_proforma_sensitivity.OperatingSensitivityTests.test_rd_change_known_ebit_effect_and_no_historical_change) ... ok
test_bad_path_and_hindsight_fail (test_revenue_forecast.RevenueTests.test_bad_path_and_hindsight_fail) ... ok
test_bad_segment_allocation_and_history_fail (test_revenue_forecast.RevenueTests.test_bad_segment_allocation_and_history_fail) ... ok
test_historical_plus_forecast_once (test_revenue_forecast.RevenueTests.test_historical_plus_forecast_once) ... ok
test_neutron_delay_removes_only_incremental_revenue (test_revenue_forecast.RevenueTests.test_neutron_delay_removes_only_incremental_revenue) ... ok
test_scenarios_are_ordered_but_not_probabilities (test_revenue_forecast.RevenueTests.test_scenarios_are_ordered_but_not_probabilities) ... ok
test_existing_forecast_round_trip_and_unchanged (test_reverse_dcf.ReverseTests.test_existing_forecast_round_trip_and_unchanged) ... ok
test_integrated_price_reproduction_and_rate_comparison (test_reverse_dcf.ReverseTests.test_integrated_price_reproduction_and_rate_comparison) ... ok
test_invalid_bounds_and_outputs (test_reverse_dcf.ReverseTests.test_invalid_bounds_and_outputs) ... ok
test_known_linear_roots_both_directions (test_reverse_dcf.ReverseTests.test_known_linear_roots_both_directions) ... ok
test_terminal_algebra_known_answer (test_reverse_dcf.ReverseTests.test_terminal_algebra_known_answer) ... ok
test_terminal_rejects_invalid_economics (test_reverse_dcf.ReverseTests.test_terminal_rejects_invalid_economics) ... ok
test_unbracketed_does_not_extrapolate (test_reverse_dcf.ReverseTests.test_unbracketed_does_not_extrapolate) ... ok
test_visible_report_preserves_rate_distinction (test_reverse_dcf.ReverseTests.test_visible_report_preserves_rate_distinction) ... ok
test_all_scenarios_balance_when_funding_is_explicit (test_three_statements.StatementTests.test_all_scenarios_balance_when_funding_is_explicit) ... ok
test_bad_paths_and_financing_inputs_fail (test_three_statements.StatementTests.test_bad_paths_and_financing_inputs_fail) ... ok
test_claim_settlement_is_not_a_second_fcff_deduction (test_three_statements.StatementTests.test_claim_settlement_is_not_a_second_fcff_deduction) ... ok
test_customer_advance_reduction_consumes_cash (test_three_statements.StatementTests.test_customer_advance_reduction_consumes_cash) ... ok
test_cutoff_claims_exclude_items_already_in_fcff (test_three_statements.StatementTests.test_cutoff_claims_exclude_items_already_in_fcff) ... ok
test_cutoff_partitions_future_flows_and_option_receipt (test_three_statements.StatementTests.test_cutoff_partitions_future_flows_and_option_receipt) ... ok
test_deliberate_cash_and_equity_corruption_fail (test_three_statements.StatementTests.test_deliberate_cash_and_equity_corruption_fail) ... ok
test_funding_failure_and_conditional_dilution_are_visible (test_three_statements.StatementTests.test_funding_failure_and_conditional_dilution_are_visible) ... ok
test_negative_fcff_preserved_even_when_accounting_profit_positive (test_three_statements.StatementTests.test_negative_fcff_preserved_even_when_accounting_profit_positive) ... ok
test_opening_reclassification_preserves_filing_and_inputs (test_three_statements.StatementTests.test_opening_reclassification_preserves_filing_and_inputs) ... ok
test_unpaid_capex_does_not_create_a_second_asset (test_three_statements.StatementTests.test_unpaid_capex_does_not_create_a_second_asset) ... ok
test_capital_overrun_reduces_value (test_valuation.ValuationTests.test_capital_overrun_reduces_value) ... ok
test_downside_funding_cannot_be_bypassed (test_valuation.ValuationTests.test_downside_funding_cannot_be_bypassed) ... ok
test_growth_direction_depends_on_economic_returns (test_valuation.ValuationTests.test_growth_direction_depends_on_economic_returns) ... ok
test_invalid_cashflow_dates_fail (test_valuation.ValuationTests.test_invalid_cashflow_dates_fail) ... ok
test_margin_shortfall_reduces_value (test_valuation.ValuationTests.test_margin_shortfall_reduces_value) ... ok
test_mixed_scenarios_fail (test_valuation.ValuationTests.test_mixed_scenarios_fail) ... ok
test_negative_2030_is_preserved_and_base_not_floored (test_valuation.ValuationTests.test_negative_2030_is_preserved_and_base_not_floored) ... ok
test_no_pre_cutoff_flows_or_duplicate_years (test_valuation.ValuationTests.test_no_pre_cutoff_flows_or_duplicate_years) ... ok
test_no_silent_input_mutation (test_valuation.ValuationTests.test_no_silent_input_mutation) ... ok
test_nonfinite_terminal_values_and_dates_fail (test_valuation.ValuationTests.test_nonfinite_terminal_values_and_dates_fail) ... ok
test_official_lab05_known_answer (test_valuation.ValuationTests.test_official_lab05_known_answer) ... ok
test_terminal_boundary_nonfinite_and_negative_profit_fail (test_valuation.ValuationTests.test_terminal_boundary_nonfinite_and_negative_profit_fail) ... ok
test_terminal_continuity_and_paid_growth (test_valuation.ValuationTests.test_terminal_continuity_and_paid_growth) ... ok
test_wacc_direction_on_selected_domain (test_valuation.ValuationTests.test_wacc_direction_on_selected_domain) ... ok
test_wacc_market_weight_and_old_erp_comparison (test_valuation.ValuationTests.test_wacc_market_weight_and_old_erp_comparison) ... ok
test_wacc_override_controls_all_validation (test_valuation.ValuationTests.test_wacc_override_controls_all_validation) ... ok

----------------------------------------------------------------------
Ran 105 tests in 2.264s

OK
```
