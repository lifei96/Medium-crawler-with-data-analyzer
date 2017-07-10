function draw_degree()
    dataset = csvread('./data/graph/degree.csv', 1, 1);
    figure(1);
    h1 = cdfplot(dataset(:,1));
    set(h1, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    xlim([0, 300]);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('In-degree','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CDF_in_degree.eps', '-depsc')
    figure(2);
    h2 = cdfplot(dataset(:,2));
    set(h2, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    xlim([0, 300]);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Out-degree','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CDF_out_degree.eps', '-depsc')
    figure(3);
    h3 = cdfplot(dataset(:,3));
    set(h3, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    xlim([0, 2])
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Balance','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CDF_balance.eps', '-depsc')
    figure(4);
    h4 = cdfplot(dataset(:,4));
    set(h4, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Reciprocity','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CDF_reciprocity.eps', '-depsc')
end