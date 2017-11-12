function draw_csl_cc()
    dataset_0 = csvread('./data/cross-site-linking/user_cc_0.csv', 1, 1);
    dataset_1 = csvread('./data/cross-site-linking/user_cc_1.csv', 1, 1);
    dataset_2 = csvread('./data/cross-site-linking/user_cc_2.csv', 1, 1);
    dataset_3 = csvread('./data/cross-site-linking/user_cc_3.csv', 1, 1);
    
    figure(1);
    a = dataset_0(:,1);
    b = a(a>=0 & a<=1);
    h = cdfplot(b);
    set(h, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    hold on;
    a = dataset_1(:,1);
    b = a(a>=0 & a<=1);
    h = cdfplot(b);
    set(h, 'color', 'r', 'LineStyle', '--', 'LineWidth', 2);
    hold on;
    a = dataset_2(:,1);
    b = a(a>=0 & a<=1);
    h = cdfplot(b);
    set(h, 'color', 'g', 'LineStyle', '-.', 'LineWidth', 2);
    hold on;
    a = dataset_3(:,1);
    b = a(a>=0 & a<=1);
    h = cdfplot(b);
    set(h, 'color', 'b', 'LineStyle', ':', 'LineWidth', 2);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Clustering Coefficient','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    legend('Neither', 'TW only', 'FB only', 'Both', 'Location', 'SouthEast');
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/csl/CDF_CC_csl.eps', '-depsc');
end